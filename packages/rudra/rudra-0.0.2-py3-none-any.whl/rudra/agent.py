import json
from typing import List, Dict, Any, Callable, Optional, Generator
import re

class Rudra:
    def __init__(self, client: Any, model: str, tools: List[Any] = None):
        self.client = client
        self.model = model
        self.tools = {}
        if tools:
            for tool in tools:
                self.add_tool(tool)

    def add_tool(self, tool: Any, name: str = None) -> None:
        if name is not None:
            self.tools[name] = tool
        elif hasattr(tool, 'name') and callable(tool.name):
            self.tools[tool.name()] = tool
        elif hasattr(tool, 'name'):
            self.tools[tool.name] = tool
        elif hasattr(tool, '__name__'):
            self.tools[tool.__name__] = tool
        else:
            raise ValueError("Tool must have a 'name' attribute or method, or be provided with a name")

    def get_llm_response(self, messages: List[Dict[str, str]], stream: bool = False) -> Any:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=stream
            )
            return response
        except Exception as e:
            return {"error": str(e)}

    def remove_comments(self, json_string: str) -> str:
        json_string = re.sub(r'//.*$', '', json_string, flags=re.MULTILINE)
        json_string = re.sub(r'/\*.*?\*/', '', json_string, flags=re.DOTALL)
        return json_string

    def parse_actions(self, response_data: Any) -> List[Dict[str, Any]]:
        if hasattr(response_data, 'choices') and response_data.choices:
            content = response_data.choices[0].message.content
        elif isinstance(response_data, dict):
            content = response_data.get('content', '')
        else:
            return [{"error": f"Unexpected response format: {response_data}"}]

        content_without_comments = self.remove_comments(content)
        
        try:
            parsed_content = json.loads(content_without_comments)
            if isinstance(parsed_content, list):
                return parsed_content
            elif isinstance(parsed_content, dict):
                if 'tool' in parsed_content and 'params' in parsed_content:
                    return [parsed_content]
                elif 'tools' in parsed_content and 'params' in parsed_content:
                    return parsed_content['params']
        except json.JSONDecodeError:
            actions = []
            pattern = r'\{[^{}]*"tool":[^{}]*"params":[^{}]*\}'
            matches = re.findall(pattern, content_without_comments)
            for match in matches:
                try:
                    action = json.loads(match)
                    actions.append(action)
                except json.JSONDecodeError:
                    pass
            
            if actions:
                return actions
        
        return [{"error": f"Failed to parse response content: {content}"}]

    def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        tool = self.tools.get(tool_name)
        if not tool:
            return {"error": f"Tool '{tool_name}' not found"}
        
        try:
            if hasattr(tool, 'execute') and callable(tool.execute):
                if isinstance(params, dict):
                    return tool.execute(**params)
                else:
                    return tool.execute(params)
            elif callable(tool):
                if isinstance(params, dict):
                    return tool(**params)
                else:
                    return tool(params)
            else:
                return {"error": f"Tool '{tool_name}' is not callable"}
        except Exception as e:
            return {"error": f"Error executing tool '{tool_name}': {str(e)}"}

    def run(self, task: str) -> Dict[str, Any]:
        return self._run_internal(task, stream=False)

    def run_stream(self, task: str) -> Generator[Dict[str, Any], None, None]:
        yield from self._run_internal(task, stream=True)

    def _run_internal(self, task: str, stream: bool) -> Any:
        tool_descriptions = "\n".join([
            f"- {name}: {tool.description() if hasattr(tool, 'description') and callable(tool.description) else (tool.__doc__ or 'No description available')}"
            for name, tool in self.tools.items()
        ])
        
        messages = [
            {"role": "system", "content": f"You are a helpful AI assistant capable of using various tools to complete tasks. Available tools:\n{tool_descriptions}\nRespond with a JSON array containing 'tool' and 'params' keys for each action. Do not include comments in the JSON."},
            {"role": "user", "content": task}
        ]
        
        response = self.get_llm_response(messages, stream=stream)
        
        if stream:
            return self._handle_stream(response)
        else:
            actions = self.parse_actions(response)
            return self._execute_actions(actions)

    def _handle_stream(self, response: Any) -> Generator[Dict[str, Any], None, None]:
        actions = []
        current_action = ""
        for chunk in response:
            if hasattr(chunk.choices[0], 'delta') and hasattr(chunk.choices[0].delta, 'content'):
                content = chunk.choices[0].delta.content
            elif hasattr(chunk, 'content'):
                content = chunk.content
            else:
                content = None

            if content:
                current_action += content
                if '}' in current_action:
                    try:
                        action = json.loads(current_action)
                        if isinstance(action, list):
                            actions.extend(action)
                        elif isinstance(action, dict):
                            actions.append(action)
                        current_action = ""
                    except json.JSONDecodeError:
                        pass
        
        for action in actions:
            if isinstance(action, dict) and "tool" in action and "params" in action:
                yield self.execute_tool(action["tool"], action["params"])
            else:
                yield {"error": f"Invalid action format. Expected 'tool' and 'params' keys. Got: {action}"}

    def _execute_actions(self, actions: List[Dict[str, Any]]) -> Dict[str, Any]:
        results = []
        for action in actions:
            if isinstance(action, dict) and "tool" in action and "params" in action:
                results.append(self.execute_tool(action["tool"], action["params"]))
            else:
                results.append({"error": f"Invalid action format. Expected 'tool' and 'params' keys. Got: {action}"})
        
        return {"results": results}