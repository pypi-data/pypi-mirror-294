# import torch 
# from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline 


# def LoadModel():
#     # Check if GPU is available
#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#     # check gpu memory ammount
#     vram = torch.cuda.get_device_properties(0).total_memory / 1024**3
#     device_ = "cuda"

#     if device.type != "cuda":
#         raise ValueError("This function is not supported on CPU")
#     if vram < 12:
#         device_ = "auto"
#         print("""

#     ECOOPEN WARNING:
#     Not enough GPU memory to run the model, switching to combined mode, which will be slower. Please use other methods (non AI) to analyze the text.

#     """)
        

#     torch.random.manual_seed(0) 
#     model = AutoModelForCausalLM.from_pretrained( 
#         "microsoft/Phi-3-mini-4k-instruct",  
#         device_map=device_,  
#         torch_dtype="auto",  
#         trust_remote_code=True,  
#     )
#     tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")
#     return model, tokenizer

# def get_inference(input_text, model):
#     model = model[0]
#     tokenizer = model[1]
#     # print(input_text)
#     answers = []
#     questions = [
#         f"Is the following text part of the scientific paper? {input_text}",
#         f"Does the following text contains information about supplementary data, data availability or a link to the data? {input_text}"
#     ]
#     for q in questions:
#         messages = [ 
#             {"role": "system", "content": "You are analyzing a possible snippet of a scientific paper. You are answering with yes and no."}, 
#             {"role": "user", "content": q},
#         ]
#         pipe = pipeline( 
#             "text-generation", 
#             model=model, 
#             tokenizer=tokenizer, 
#         )
#         generation_args = { 
#             "max_new_tokens": 500, 
#             "return_full_text": False, 
#             "temperature": 0.1, 
#             "do_sample": False, 
#         }
#         output = pipe(messages, **generation_args ) 
#         answers.append(output[0]['generated_text'])
        
#     return answers

# if __name__=="__main__":
#     # create_model()
#     print(get_inference("Data is available at the paper website. The link is www.sciom.hr/data/data.csv"))