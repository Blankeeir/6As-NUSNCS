from typing_extensions import override
from openai import AssistantEventHandler
from multiprocessing import Queue
 
# First, we create a EventHandler class to define
# how we want to handle the events in the response stream.

class EventHandler(AssistantEventHandler):    
    def __init__(self):
        self.queue = Queue()
        super().__init__()
  
    def get_consumer(self):
      def consumer():
        while True:
          message = self.queue.get()
          if isinstance(message, str):
            yield message.encode('utf-8')  # Convert message to bytes
          else:
            yield message

      return consumer
    
    @override
    def on_text_created(self, text) -> None:
        return
        #self.queue.put(text)

    @override
    def on_text_delta(self, delta, snapshot):
        self.queue.put(delta.value)

    def on_tool_call_created(self, tool_call):
        self.queue.put(tool_call.type)

    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                self.controller.output = delta.code_interpreter.input
            if delta.code_interpreter.outputs:
     
                self.controller.output = "\n\noutput >"
    
    def close(self):
        self.queue.close()
        super().close()

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