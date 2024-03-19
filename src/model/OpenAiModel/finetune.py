from openai import OpenAI













# Code here for file upload (fine-tuning purpose)



class finetuneWithFile(object):
    


    def __init__(self,training_file,model):
        super().__init__()
        self.training_file = training_file
        self.model = model

    def create_finetune(self):
        client = OpenAI(
            # This is the default and can be omitted
            api_key=os.environ.get("OPENAI_API_KEY")  # see .env
        )
        
        response = client.fine_tuning.jobs.create(
            training_file=self.training_file,
            model=self.model
        )

        return response


