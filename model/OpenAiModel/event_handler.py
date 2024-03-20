from typing_extensions import override
from openai import AssistantEventHandler
 
# First, we create a EventHandler class to define
# how we want to handle the events in the response stream.

class EventHandler(AssistantEventHandler):    
    def __init__(self):
        self.output = ""
        self.isProcessing = True
        super().__init__()

    @override
    def on_text_created(self, text) -> None:
        self.output += f"\nassistant > "

    @override
    def on_text_delta(self, delta, snapshot):
        self.output += delta.value

    def on_tool_call_created(self, tool_call):
        self.output += f"\nassistant > {tool_call.type}\n"

    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                self.output += delta.code_interpreter.input
            if delta.code_interpreter.outputs:
     
                self.output += "\n\noutput >"
    '''
    @override
    def close(self):
        self.isProcessing = False
        super().close()'''




'''
class EventHandler(AssistantEventHandler):

    def __init__(self):    
  @override
  def on_text_created(self, text) -> None:
    print(f"\nassistant > ", end="", flush=True)
      
  @override
  def on_text_delta(self, delta, snapshot):
    print(delta.value, end="", flush=True)
      
  def on_tool_call_created(self, tool_call):
    print(f"\nassistant > {tool_call.type}\n", flush=True)
  
  def on_tool_call_delta(self, delta, snapshot):
    if delta.type == 'code_interpreter':
      if delta.code_interpreter.input:
        print(delta.code_interpreter.input, end="", flush=True)
      if delta.code_interpreter.outputs:
        print(f"\n\noutput >", flush=True)
        for output in delta.code_interpreter.outputs:
          if output.type == "logs":
            print(f"\n{output.logs}", flush=True)

'''