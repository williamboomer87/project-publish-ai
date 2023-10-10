import numpy as np
import gradio as gr
import textwrap
import openai
import json


from googlesearch import search
import requests
from bs4 import BeautifulSoup
#import openai
#import textwrap

#def transcribe_audio(audio_file):
   # return true


def flip_image(x):
    return np.fliplr(x)



with gr.Blocks() as demo:
    
    gr.Markdown("""
    # Publish-AI Email and Press Release
    Select Email or Press Release
    """)
    with gr.Accordion("Content Generation"):
       # gr.Markdown("Email Release , Press Release ")

        with gr.Tab("Email Release"):
            with gr.Row():
                with gr.Column(scale=1, min_width=600):
                
                    # Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
                    openai.api_key = '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'
                    #, benefits , unique_selling_point , pain_point , emotion
                    # Function to generate a press release based on user inputs
                    def generate_press_release(product, advantages, story, desire, ideal_customer_personal, 
                                            problem, interest, desired_action, name1, name, tone):
                        try:
                            # Save input data in a dictionary
                            input_data = {
                                'product': product,
                                'advantages': advantages,
                                #'benefits': benefits,
                                'story': story,
                                'desire': desire,
                                'ideal_customer_personal': ideal_customer_personal,
                                'problem': problem,
                                'interest': interest,
                                #'unique_selling_point': unique_selling_point,
                                'desired_action': desired_action,
                                #'pain_point': pain_point,
                                #'emotion': emotion,
                                'name1': name1,
                                'name': name,
                                'tone': tone
                            }
                    
                            # Convert input data to a JSON string
                            input_data_json = json.dumps(input_data)
                    
                            # Define the template with placeholders for user inputs
                            prompt_text = f"""
                            Imagine you are a skilled public relations expert with years of experience in creating captivating emails that generate interest and coverage. You have been tasked with writing an email for:
                            {input_data_json}
                    
                            Introduction: [We are thrilled to announce that on {product}, it has many {advantages}, {product} is unveiling a groundbreaking initiative: {product}. This initiative reaffirms our commitment to delivering high-quality [Benefits]. this is about [Story]]
                            Body: [The {product} offers a {desired_action} by allowing our valued {ideal_customer_personal}.]
                            Overview: [There are some {problem}. But these can {interest} solve it. It has some new things and say about it. So we are looking to get {desired_action}.]
                    
                            Task Requirements:Need to follow the below structure is must every square brackets. use {tone} tone to write the email. email should be between 750 - 900 letters.
                    
                            Subject: About Our New Announcement
                    
                            Dear {name},
                    
                            Compose an email to inform {name1} about our new {product}. The email should start with a warm greeting and express enthusiasm about the announcement. [Introduction] should briefly introduce {product} and highlight its uniqueness and relevance to the industry it belongs to.
                    
                            In the body of the email, provide a detailed [Body] of {product}, including its key features, benefits, and any notable improvements or innovations. Use clear and concise language to explain why {product} stands out and how it can address the needs or pain points of potential customers.
                    
                            [Overview] write at least 2 paragraphs.
                    
                            Conclude the email by expressing gratitude for the recipient's support and interest, and mention that more updates about {product} will be shared in the future.
                    
                            Please ensure that the email is professional, engaging, and informative, while maintaining a {tone} tone throughout.
                    
                            Sincerely,\n
                            {name1}
                            """
                    
                            # Use GPT-3.5 Turbo to generate the press release
                            response = openai.Completion.create(
                                engine="text-davinci-003",  # GPT-3.5 Turbo engine
                                prompt=prompt_text,
                                max_tokens=2500,  # Set the desired press release length
                                temperature=0.9,  # Adjust the temperature for creativity
                            )
                    
                            # Extract the generated press release from the GPT-3.5 Turbo response
                            press_release = response['choices'][0]['text'].strip() # Remove leading and trailing whitespace
                            press_release.strip("\t")
                            return press_release  # Return the press release
                        except Exception as e:
                            return str(e)
                    
                    
                        # Create a Gradio interface using Blocks
                    with gr.Blocks() as main_window:
                        gr.Markdown("# Email Generator")
                        gr.Markdown("Generate a Email based on your inputs and save input data in JSON format.")
                        
                        with gr.Row():
                            with gr.Column():
                                

                                product = gr.Textbox(label="Service or Product Name", value="Children's Reading Book")
                                #product= gr.Dropdown(choices=["Children's Reading Book","Book Launch","Branding Services"],label="Service or Product Name" , allow_custom_value=True)
                                advantages= gr.Dropdown(choices=["Be the first to receive it","Collect your order", "Find the useful one"],label="Service or Product Advantages" , allow_custom_value=True)
                                #benefits = gr.Dropdown(choices=["Can read","Motivational One","Can share with others"],label="Service or Product Benefits")
                                story= gr.Dropdown(choices=["Generate a story about Children's Reading Book and its name is Childhood Life","Generate a good artical about it","Tell some nice story for this"],label="Service or Product Story" ,allow_custom_value=True) 
                                desire= gr.Dropdown(choices=["Experience convenience","Capture memories in here","Stay connected with loved ones effortlessly"],label="Desired Outcome or Experience" , allow_custom_value=True)
                                ideal_customer_personal=gr.Dropdown(choices=["Meet our branch in charge","Meet our HR Manager","Connect with customer service"],label="Ideal Customer Personal (Whom you should contact within the firm)" , allow_custom_value=True) 
                                problem=gr.Dropdown(choices=["Stories are horror content based", "Many negative roles","Some stories are not realistic"],label="Problem Addressed" ,allow_custom_value=True)
                                interest=gr.Dropdown(choices=["You’ll love to read it","You can enjoy it","Can find the joy over here"],label="Why People Would Be Interested", allow_custom_value=True)
                                #unique_selling_point=gr.Dropdown(choices=["Our books are #1 selling in USA","Our service is #1 selling in USA","We are the best in the region"],label="Unique Selling Point")
                                desired_action=gr.Dropdown(choices=["Don’t miss out on the opportunity to order your book","Be the first to grab it","Try to get your E-book"],label="Desired Call to Action",allow_custom_value=True)
                                #pain_point=gr.Dropdown(choices=["Clarity and Comprehension","Measuring Impact","Accessibility"],label="Pain Point Alleviated")
                                #emotion=gr.Dropdown(choices=["Experience the thrill of futuristic driving while honoring your commitment","Ignite the flames of curiosity and bask in the glory of  achievements","Embark on a journey where every step is a celebration of your strength with us"],label="Emotion Associated")
                                name1 = gr.Textbox(label="Sender's Name" , value="Sara")
                                #name1=gr.Dropdown(choices=["Johna","Jack","Thomas"],label="Recipient Name")
                                name = gr.Textbox(label="Recipient Name" , value="Joseph")
                                #name=gr.Dropdown(choices=["Anna","Joseph","John"],label="Sender's Name")
                                tone=gr.Dropdown(choices=["Formal"," Informal","Friendly","Diplomatic","Inspirational"],label="Tone of the Email" , allow_custom_value=True)


                                
                                #product = gr.Textbox(label="Product Name", value="Children's Reading Book")
                                #advantages = gr.Textbox(label="Product Advantages", value="can read,can enjoy")
                                #benefits = gr.Textbox(label="Product Benefits", value="can read,can give to others and can make everyone surprise")
                                #story = gr.Textbox(label="Product Story", value="generate a story about Children's Reading Book and its name is Childhood Life")
                                #desire = gr.Textbox(label="Desired Outcome or Experience", value="Experience convenience, capture memories, and stay connected with loved ones effortlessly")
                                #ideal_customer_personal = gr.Textbox(label="Ideal Customer Personal", value="Meet Anna,Our branch incharge")
                                #problem = gr.Textbox(label="Problem Addressed", value="Stories are horror content based")
                                #interest = gr.Textbox(label="Why People Would Be Interested" , value="You’ll love to read it")
                                #unique_selling_point = gr.Textbox(label="Unique Selling Point", value="Our books are #1 selling in newyork")
                                #desired_action = gr.Textbox(label="Desired Action", value="Don’t miss out on the opportunity to order your book")
                                #pain_point = gr.Textbox(label="Pain Point Alleviated", value="Dealing with a slow and battery-hungry peoples")
                                #emotion = gr.Textbox(label="Emotion Associated" , value="Experience the joy of capturing life’s moments in stunning detail and the relief of having a phone that keeps up with your demand")
                                #name1 = gr.Textbox(label="Your Name" , value="Sara")
                                #name = gr.Textbox(label="Sender's Name" , value="Joseph")
                                #tone = gr.Radio(label="Tone of the Email", choices=["Formal", "Friendly"])
                                
                            with gr.Column():
                                with gr.Row():
                                    btn = gr.Button("Generate Email")
                                with gr.Row():
                                    output = gr.Textbox(label="Generated Email")
                                
                        
            btn.click(fn=generate_press_release, 
                        inputs=[product, advantages, story, desire, ideal_customer_personal, 
                                problem, interest, desired_action, 
                                name1, name, tone], 
                        outputs=output)
    #, unique_selling_point
    #benifits
    #, pain_point
    #emotion
    #main_window.launch(share=True)

                    
                #main_window.launch(share=True)

                    #text1 = gr.Textbox(label="One")
                    #text2 = gr.Textbox(label="Two")
                    #text3 = gr.Textbox(label="Three")
                    #tone_type = gr.CheckboxGroup(["Formal", "Friendly"])
                    
                #with gr.Column(scale=1, min_width=600):
                    #Output = gr.Textbox(label="One")
        with gr.Tab("Press Release"):
                with gr.Column(scale=1, min_width=600):
                    
                    # Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
                    openai.api_key = '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'
                    
                    def generate_press_release(
                        company,
                        industry,
                        announcement,
                        event_initiative_product,
                        date,
                        city,
                        key_benefits_highlights,
                        quotes,
                        contact_information,
                        email,
                        website,
                        name,
                        #phone,
                    ):
                        try:
                            # Construct the prompt using user-provided values
                            prompt_text = f"""
                            "Press release Prompt
                            Imagine you are a skilled public relations expert with years of experience in
                            creating captivating press releases that generate interest and coverage. You
                            have been tasked with writing a press release for:
                            Company: {company}
                            Industry: {industry}
                            Announcement: {announcement}
                            Event/Initiative/Product: {event_initiative_product}
                            Date: {date}
                            City: {city}
                            Key Benefits/Highlights: {key_benefits_highlights}
                            Quotes: {quotes}
                            Contact Information: {contact_information}
                            Email: {email}
                            Website: {website}
                            Name : {name}
                            Task Requirements:
                            Add text 'For Immediate Release'
                    
                            Headline: Craft a compelling and professional headline that captures the essence of the announcement and generates interest and its Immediate Press Release.
                    
                            Subheading: Provide a subheading that further elaborates on the headline and offers additional context.
                    
                            Introduction: Write an opening paragraph that summarizes the key points of the announcement. Write this for 3 paragraphs.
                    
                            Body: Expand on the details of the announcement, highlighting the key benefits,and providing relevant quotes from spokesperson(s).
                            
                            Company Description/About the Company: Include a brief overview of the company,its history, and mission.
                            
                            Contact Information:
                            Name: {name}
                            Phone: {contact_information}
                            Email: {email}
                            Website: {website}
                            arrange this Contact Information details one over one.
                            """
                            
                            # Use GPT-3.5 Turbo to generate the press release
                            response = openai.Completion.create(
                                engine="text-davinci-003",  # GPT-3.5 Turbo engine
                                prompt=prompt_text,
                                max_tokens=2500,  # Set the desired press release length
                                temperature=0.9,  # Adjust the temperature for creativity
                            )
                    
                            # Extract the generated press release from the GPT-3.5 Turbo response
                            press_release = response['choices'][0]['text'].strip() 
                            press_release.strip("\t")
                            return press_release
                        except Exception as e:
                            return str(e)
                    
                    # Create a Gradio interface using Blocks
                    with gr.Blocks() as main_window:
                        gr.Markdown("# Press Release Generator")
                        gr.Markdown("Generate a press release with user-provided information.")
                        
                        with gr.Row():
                            with gr.Column():

                                #company= gr.Dropdown(choices=["Chelsea's New Beginning","Emirates","Edna"],label="Company Name")
                                #industry = gr.Dropdown(choices=["Publishers","Airline","Markerting"],label="Industry")
                                #announcement = gr.Dropdown(choices=["Get your order","Be first","take your chance"],label="Announcement")
                                #event_initiative_product=gr.Dropdown(choices=["Pay Per book","Pay per ticket","Pay per news"],label="Event/Initiative/Product")
                                #date = gr.Dropdown(choices=["Oct 3 2023","Oct 4 2023","Oct 5 2023"],label="Date")
                                #city = gr.Dropdown(choices=["London","New York","Texas"],label="City")
                                #key_benefits_highlights = gr.Dropdown(choices=["#1 Sellers in books","We are the best in USA","We are best in our region"],label="Key Benefits/Highlights")
                                #quotes = gr.Dropdown(choices=["Good Books","Nice Work","Love to See"],label="Quotes")
                                #contact_information =gr.Dropdown(choices=["70-55-1212","88-55-1542","66-55-5645"],label="Contact Information")
                                #email=gr.Dropdown(choices=["chelseasnewbeginning@yahoo.com","emirates@gmail.com","edna@hotmail.com"],label="Email")
                                #website = gr.Dropdown(choices=["www.chelseasnewbeginning.com","www.emirates.com","www.edna.com"],label="Website")
                                #name = gr.Dropdown(choices=["John","Anna","Thomas"],label="Name")
                                #phone = gr.Dropdown(choices=["737-90-8973","787-90-7876","432-90-8872"],label="Phone")
                                
                                company = gr.Textbox(label="Company", value="Chelsea's New Beginning")
                                industry = gr.Dropdown(choices=["Publishers","Airline","Markerting"],label="Industry" , allow_custom_value=True)
                                #industry = gr.Textbox(label="Industry", value="Publishers")
                                announcement = gr.Textbox(label="Announcement", value="Childrens Story book")
                                event_initiative_product = gr.Textbox(label="Event/Initiative/Product" , value="Pay Per book")
                                date = gr.Textbox(label="Date", value="Feb 2 2022")
                                city = gr.Textbox(label="City" , value="London")
                                key_benefits_highlights = gr.Textbox(label="Key Benefits/Highlights", value="#1 Sellers in books")
                                quotes = gr.Textbox(label="Quotes", value="Good Books")
                                contact_information = gr.Textbox(label="Contact Information", value="670-55-1212")
                                email = gr.Textbox(label="Email", value="chelseasnewbeginning@yahoo.com")
                                website = gr.Textbox(label="Website", value="www.chelseasnewbeginning.com")
                                name = gr.Textbox(label="Name", value="Joseph")
                                #phone = gr.Textbox(label="Phone", value="787-90-7876")
                            with gr.Column():
                                with gr.Row():
                                    btn = gr.Button("Generate Press Release") 
                                with gr.Row():                             
                                    output = gr.Textbox(label="Generated Press Release")
                        
        btn.click(fn=generate_press_release, 
                    inputs=[company, industry, announcement, event_initiative_product, date, city, 
                            key_benefits_highlights, quotes, contact_information, email, website, 
                            name], 
                    outputs=output)
                        #, phone

        with gr.Tab("Email Template 1"):
            #gr.Column()
            openai.api_key = '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'
                #, benefits , unique_selling_point , pain_point , emotion
                # Function to generate a press release based on user inputs
            with gr.Column():
                    def generate_press_release(event, alert, story, name1, name, tone):
                        try:
                            # Save input data in a dictionary
                            input_data = {

                                'event': event,
                                'alert':alert,
                                'story': story,
                                'name1': name1,
                                'name': name,
                                'tone': tone
                                
                                
                            }
                    
                            # Convert input data to a JSON string
                            input_data_json = json.dumps(input_data)
                    
                            # Define the template with placeholders for user inputs
                            prompt_text = f"""
                            Imagine you are a skilled public relations expert with years of experience in creating captivating emails that generate interest and coverage. You have been tasked with writing an email for:
                            {input_data_json}
                            
                            Subject: About Our New Announcement

                            Body: [write about the {event} and  give me the brieaf details regarding it.]

                            Introduction: [describe about {event} and write about this, write about this,This initiative reaffirms our commitment to delivering high-quality about this.]

                            Overview: [There are some {alert}. mention these in in bold and red colour]

                            Task Requirements:Need to follow the below structure is must every square brackets. use {tone} tone to write the email. email should be between 750 - 900 letters.
                    
                            [Subject] Must be here
                    
                            Dear {name},
                    
                            Compose an email to inform {name1} about our new {event}. The email should start with a warm greeting and express enthusiasm about the announcement. [Introduction] should briefly introduce {event} and highlight its uniqueness and relevance to the industry it belongs to.
                    
                            In the body of the email, provide a detailed [Body] of {event}, including its key features, benefits, and any notable improvements or innovations. Use clear and concise language to explain why {event} stands out and how it can address the needs or pain points of potential customers.
                    
                            [Overview] write at least 2 paragraphs.
                    
                            Conclude the email by expressing gratitude for the recipient's support and interest, and mention that more updates about {event} will be shared in the future.
                    
                            Please ensure that the email is professional, engaging, and informative, while maintaining a {tone} tone throughout.
                    
                            Sincerely,\n
                            {name1}
                            Ensure the above structure throughly. 
                            Give this as formated html as output.
                            """
                    
                            # Use GPT-3.5 Turbo to generate the press release
                            response = openai.Completion.create(
                                engine="text-davinci-003",  # GPT-3.5 Turbo engine
                                prompt=prompt_text,
                                max_tokens=2500,  # Set the desired press release length
                                temperature=0.9,  # Adjust the temperature for creativity
                            )
                    
                            # Extract the generated press release from the GPT-3.5 Turbo response
                            press_release = response['choices'][0]['text'].strip() # Remove leading and trailing whitespace
                            press_release.strip("\t")
                            return press_release  # Return the press release
                        except Exception as e:
                            return str(e)
                    
                    
                        # Create a Gradio interface using Blocks
                    with gr.Blocks() as main_window:
                        gr.Markdown("# Virtual Event Secret Email")
                        gr.Markdown("Generate a Email based on your inputs.")
                        
                        with gr.Row():
                            with gr.Column():
                                
                                
                                event = gr.Textbox(label="Add event details", value="")
                                #product= gr.Dropdown(choices=["Children's Reading Book","Book Launch","Branding Services"],label="Service or Product Name" , allow_custom_value=True)
                                #advantages= gr.Dropdown(choices=["Be the first to receive it","Collect your order", "Find the useful one"],label="Service or Product Advantages" , allow_custom_value=True)
                                #benefits = gr.Dropdown(choices=["Can read","Motivational One","Can share with others"],label="Service or Product Benefits")
                                story = gr.Textbox(label="Tell About Event Story", value="")
                                alert = gr.Textbox(label="Add important message over here", value="")
                                #ideal_customer_personal=gr.Dropdown(choices=["Meet our branch in charge","Meet our HR Manager","Connect with customer service"],label="Ideal Customer Personal (Whom you should contact within the firm)" , allow_custom_value=True) 
                                #problem=gr.Dropdown(choices=["Stories are horror content based", "Many negative roles","Some stories are not realistic"],label="Problem Addressed" ,allow_custom_value=True)
                                #interest=gr.Dropdown(choices=["You’ll love to read it","You can enjoy it","Can find the joy over here"],label="Why People Would Be Interested", allow_custom_value=True)
                                #unique_selling_point=gr.Dropdown(choices=["Our books are #1 selling in USA","Our service is #1 selling in USA","We are the best in the region"],label="Unique Selling Point")
                                #desired_action=gr.Dropdown(choices=["Don’t miss out on the opportunity to order your book","Be the first to grab it","Try to get your E-book"],label="Desired Call to Action",allow_custom_value=True)
                                #pain_point=gr.Dropdown(choices=["Clarity and Comprehension","Measuring Impact","Accessibility"],label="Pain Point Alleviated")
                                #emotion=gr.Dropdown(choices=["Experience the thrill of futuristic driving while honoring your commitment","Ignite the flames of curiosity and bask in the glory of  achievements","Embark on a journey where every step is a celebration of your strength with us"],label="Emotion Associated")
                                name1 = gr.Textbox(label="Sender's Name" , value="Sara")
                                #name1=gr.Dropdown(choices=["Johna","Jack","Thomas"],label="Recipient Name")
                                name = gr.Textbox(label="Recipient Name" , value="Joseph")
                                #name=gr.Dropdown(choices=["Anna","Joseph","John"],label="Sender's Name")
                                tone=gr.Dropdown(choices=["Formal"," Informal","Friendly","Diplomatic","Inspirational"],label="Tone of the Email" , allow_custom_value=True)
  
                        with gr.Column():
                                btn = gr.Button("Generate Email")
                                output = gr.HTML(label="Generated Email")
                                
                        
                        btn.click(fn=generate_press_release, 
                                inputs=[event,alert, story, 
                                        name1, name, tone], 
                                outputs=output)

    with gr.Accordion("Article Generation"):

            with gr.Tab("Article Generation"):
                # Define your OpenAI API key here
                openai.api_key = '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'  # Replace with your key
                
            def get_google_search_results(keyword, num_results=12):
                try:
                    results = []
                    for result in search(keyword, num_results=num_results):
                        results.append(result)
                    return results
                except Exception as e:
                    print(f"An error occurred while fetching Google search results: {str(e)}")
                    return None

            def scrape_content(link):
                try:
                    response = requests.get(link)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    paragraphs = soup.find_all('p')
                    content = "\n".join([p.get_text() for p in paragraphs])
                    return content
                except Exception as e:
                    print(f"An error occurred while scraping content from {link}: {str(e)}")
                    return None

            def generate_article_from_keyword(keyword):
                search_links = get_google_search_results(keyword)

                if search_links:
                    scraped_content = [scrape_content(link) for link in search_links]
                    meaningful_content = "\n".join(scraped_content)  # Combine all scraped content

                    # Structured prompt for generating article
                    prompt_text = f"""
                    Article Generating Prompt

                    Imagine you are a seasoned technology journalist with a knack for unveiling the impacts of innovative breakthroughs on our daily lives. Your task is to generate an article that explores a groundbreaking technological advancement:

                    

                    Ensure the article adheres to the following structure:

                    Task Requirement: Develop 2-3 paragraphs for each section, ensuring clarity and a well-structured output. The total word count should be between 1200-1800 words.


                    Heading:

                    Create an insightful and engaging headline that encapsulates the significance of the technological breakthrough and sparks curiosity.


                    Subheading: 

                    [Craft a subheading that delves deeper into the headline, providing additional insights.]

                    Compose 2-3 paragraphs that furnish further details and context to bolster the headline.


                    Introduction: 

                    [Pen an initial paragraph that encapsulates the crucial aspects of the technological breakthrough.]

                    Expand this section into 2-3 paragraphs, ensuring a coherent flow of information and a robust commencement to the article.


                    Body: 

                    [Delve into the particulars of the technological advancement, emphasizing its key implications, and incorporating pertinent quotes from experts or industry leaders.]

                    Ensure this section is thorough and offers a holistic view of the technological breakthrough in 2-3 paragraphs.


                    Impact Analysis: 

                    [Provide a succinct overview of the potential impacts of the technology on various sectors and the general populace.]

                    Develop this into 2-3 paragraphs, offering a detailed analysis and possibly including real-world applications or future projections of the technology.


                    Conclusion: 

                    [Conclude by summarizing the key points and potentially providing a viewpoint on the future implications of the technology.]

                    Ensure the conclusion effectively encapsulates the article and offers a clear closure in 2-3 paragraphs.

                    Give this as formated html as output.
                    """




                    # Ensure the total tokens are within the model's limit
                    max_tokens_for_content = 4097 - len(prompt_text) - 100  # 100 is a buffer for additional tokens in API calls
                    truncated_content = meaningful_content[:max_tokens_for_content]

                    # Combine the structured prompt with the scraped content and keyword
                    prompt = f"Topic: {keyword}\n\nScraped Content:\n{truncated_content}\n\n{prompt_text}\n\n"
                    
                    # Generate text using OpenAI API
                    response = openai.Completion.create(
                        engine="text-davinci-003",
                        prompt=prompt,
                        max_tokens=1200
                    )
                    generated_article = response.choices[0].text.strip()

                    # Return the generated article
                    wrapped_article = textwrap.fill(generated_article, width=80)
                    return wrapped_article
                else:
                    return "No search results found."

            keyword_input = gr.Textbox(label="Enter a keyword to generate an article:")
            article_btn = gr.Button("Generate Article")
            output_article = gr.HTML(label="Generated Article")

            article_btn.click(generate_article_from_keyword, inputs=keyword_input, outputs=output_article)                           

if __name__ == "__main__":
    demo.launch(share=True)
