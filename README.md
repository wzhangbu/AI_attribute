# HO_AI_Property_Attribute_2025


### Important Locations
S3 working folder:  s3://pr-home-datascience/Projects/AdHoc/InternProjects/2025/2025_Summer_AI_Property_Attributes/

slides: https://plymouthrock.sharepoint.com/:f:/s/Home-DataScience/El5yWmPeXQlHsXPTk16oqbIBGgn5jil3ZevJ-5J5-58OXA?e=iIhgVR

OneNote: [onenote:#2025%20Summer%20AI%20Property%20Attributes&section-id={EE1A4C04-AC27-4C11-8A8A-CF8905A19118}&page-id={C4CF00A3-3B5D-499E-A5B1-99E4B0BBF087}&end&base-path=https://plymouthrock.sharepoint.com/sites/Home-DataScience/Shared%20Documents/data%20science%20project%20summary/adHoc.one](https://plymouthrock.sharepoint.com/:o:/r/sites/Home-DataScience/_layouts/15/doc2.aspx?sourcedoc=%7B584019F2-1FB1-4A87-9216-257392EFAA58%7D&wd=target(adHoc.one%7CEE1A4C04-AC27-4C11-8A8A-CF8905A19118%2F2025%20Summer%20AI%20Property%20Attributes%7CC4CF00A3-3B5D-499E-A5B1-99E4B0BBF087%2F)&wdpartid=%7B40DD89BE-1862-0893-2AA3-B877F6BF00ED%7D%7B1%7D&wdsectionfileid=%7B12D623D1-1115-4072-A51F-AB125D049ADC%7Donenote%3Ahttps%3A%2F%2Fplymouthrock.sharepoint.com%2Fsites%2FHome-DataScience%2FShared%20Documents%2Fdata%20science%20project%20summary%2FadHoc.one)



### Prerequisites
- Python 3.12.9  
- AWS Account with S3 access  
- OpenAI API Key for AI-based image analysis  
- Python libraries (see details in the Jupyter file)  

### Core Project Steps

1. **Load Data**
   - Use the Python file `read_data.py` to load the samples file from Shawn: `./property_list_NJ_sample.csv`.  
     **Input**: `DataReader(file_path)`  
     **Output**: `DataReader.path`, `DataReader.data`

2. **Generate GPT Model**
   - Use `GPT_model.py`. The default model is `'gpt-4.1'` and the API key is from Shawn.  
     a. The `general_input` function defines the format-prompt for GPT before questions.  
     b. The `estimate_all` function sends questions for all addresses. It will mark `NaN` for missing address info.

3. **Ask GPT**
   - Follow `ask_GPT.ipynb` to generate GPT responses, combined with the Excel provided by Shawn.  
     a. Generates the Excel file `./results/data_all_n1000.xlsx` by default.  
     b. Change `n` to 2000 to generate all predictions.

4. **Statistical Analysis**
   - Follow `statistic_analysis.ipynb` to compare GPT predictions with Quantarium data.  
     a. Produces a histogram of differences and a confusion matrix.  
     b. Both are used in the final presentation.

5. **Prediction Evaluation**
   - Follow `prediction.ipynb` to evaluate GPT predictions:  
     a. Consistency across multiple prompts.  
     b. Performance on datasets with and without Quantarium information.

### Notes

1. The default model is `'gpt-4.1'`; `'gpt-4o'` may not yield good results.  
2. Skip `NaN` entries from Shawn’s address file during prompting.  
3. Use Python to generate an editable Excel histogram for the presentation slides.  
4. GPT run time:  
   - ~38 min for 1000 questions  
   - ~58 min for 2000 questions  
5. Validate GPT and Quantarium data with external sites (e.g., Zillow, Redfin).

