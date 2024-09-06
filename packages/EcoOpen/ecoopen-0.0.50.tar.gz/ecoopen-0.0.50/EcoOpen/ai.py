# from EcoOpen.inference import get_inference
# from EcoOpen.core import ReadPDF
# from tqdm import tqdm
# import re
# from pprint import pprint
# import os
# import torch
# from transformers import BertTokenizer, BertForSequenceClassification

# def AnalyzePDF_AI(filepath, model):
#     raw = ReadPDF(filepath)
#     # split text into sentences
#     sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', raw)
#     # pprint(sentences)

#     # split raw into paragraphs made from 5 sentences
#     paragraphs = []
#     for i in range(0, len(sentences), 3):
#         paragraph = " ".join(sentences[i:i+5])
#         paragraphs.append(paragraph)

#     # get inference
#     inference = []
#     for i in tqdm(paragraphs):
#         inf = get_inference(i, model)
#         # print("Sentece", i)
#         # print("Inference", inf)
#         inference.append([i, inf])

#     inference = inference_cleanup(inference)
    
#     return inference

# def inference_cleanup(inference):
#     new_inference = []
#     for i in inference:
#         i_=[i[0]]
#         if "yes" in i[1][0].lower():
#             i_.append("yes")
#         elif "no" in i[1][0].lower():
#             i_.append("no")

#         if "yes" in i[1][1].lower():
#             i_.append("yes")
#         elif "no" in i[1][1].lower():
#             i_.append("no")

#         new_inference.append(i_)
#     return new_inference


# def find_dataAI(path):
#     inference = AnalyzePDF_AI(path, model)
#     indices = find_supplementary_data_sentence_AI(inference)
#     data_links = []
#     dataframe = {
#         "data_links": [],
#         "inference": []
#     }
#     if indices != []:
#         for i in indices:
#             # detect http links
#             link = re.findall(r'(https?://\S+)', inference[i][0])
#             if link != []:
#                 data_links.append(link)

#         dataframe["data_links"] = data_links
#         dataframe["inference"] = inference[i]

#         return dataframe

#     else:
#         print("No supplementary data found or data reference found in this paper")
#         return None

# def find_supplementary_data_sentence_AI(inference):
#     indices = []
#     for idx, i in enumerate(inference):
#         if "yes" in i[2].lower():
#             indices.append(idx)
#     return indices