import numpy as np
import gradio as gr
import textwrap
import openai
import json
from langchain.document_loaders import AsyncChromiumLoader
from langchain.document_transformers import BeautifulSoupTransformer
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage


from googlesearch import search
import requests
from bs4 import BeautifulSoup
#import openai
#import textwrap

#def transcribe_audio(audio_file):
   # return true
key = 'Add_Your_Api_Key'

def flip_image(x):
    return np.fliplr(x)



with gr.Blocks() as demo:
    
    gr.Markdown("""
    # Publish-AI Creations
    Select Press Release , Email Generation and Article Generation
    """)
    with gr.Accordion("Press Release"):
     
        with gr.Tab("Press Release"):
                with gr.Column(scale=1, min_width=600):
                    
                    # Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
                    openai.api_key = key
                    
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

        
    with gr.Accordion("Email Templates"):      

        with gr.Tab("Email Generation"):
            with gr.Column():
                
                    # Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
                    openai.api_key = key
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
                                tone=gr.Dropdown(choices=["Formal"," Informal","Friendly","Diplomatic","Inspirational"],label="Tone of the Email" , allow_custom_value=True,value="Formal")
                                #gr.ClearButton(product,tone,name,story,desire,ideal_customer_personal,problem,interest,desired_action,name1)

                                
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
        

        with gr.Tab("Email Template 1"):

            openai.api_key = key
                #, benefits , unique_selling_point , pain_point , emotion
                # Function to generate a press release based on user inputs
            with gr.Column():
                    def generate_press_release(your_first_name, insert_problem, desire, cus_prob, prod_name, page_url,tone):
                        try:
                            # Save input data in a dictionary
                            input_data = {
            
                                'your_first_name': your_first_name,
                                'insert_problem':insert_problem,
                                'desire': desire,
                                'cus_prob': cus_prob,
                                'prod_name': prod_name,
                                'page_url': page_url,
                                'tone': tone
                                
                            }
                    
                            # Convert input data to a JSON string
                            input_data_json = json.dumps(input_data)
                    
                            # Define the template with placeholders for user inputs
                            prompt_text = f"""
                            Imagine you are a skilled public relations expert with years of experience in creating captivating emails that generate interest and coverage. You have been tasked with writing an email for:
                            {input_data_json}
                            
                            Subject Line:  BOOM - its going to blow up!The true secret of success.
            
                            Hey! {your_first_name} here and I know if you are reading this you have probably struggled with {insert_problem} just like everyone else on my list.
            
                            I’m over the moon you’re here cause we don’t need to struggle with that ANY more!!
                            
                            You must be ready to roll up your sleeves and get down to business.
            
                            But…
            
                            Before you start moving toward {desire}
            
                            I want to give you fair warning
                            
                            There are a lot of claims on the Internet to help you be more successful at {cus_prob}.
                            
                            Expensive ones. Most, gimmicks designed to suck your bank account dry.
                            
                            Do they work?
                            
                            Who really knows?
                            
                            Neither you nor I, have time to dilly dally or debate.
                            
                            My goal is simple… Save you time, energy, and money.
            
                            You see, so many people get lost in the vortex of “shiny object” syndrome, signing up for every list, downloading every freebie, and buying tons of products, none of which they use.
            
                            It’s really sad to see.
                            
                            That’s exactly why I came up with {prod_name}.
                            
                            It gives you everything you need to solve {cus_prob}, and get the success you are after.
            
                            Here’s the deal.
            
                            When you join us you’ll discover…
            
                            > A quick and easy way to {desire}[customer’s desired result]
            
                            > How to stop {cus_prob}, and start winning
            
                            Is this something you want?
            
                            If yes, you know what to do.
                            
                            Click here 
                            {page_url}
            
                            There you will find everything you need to get even farther on this success path.
            
                            It’s time for you to get the results you want without all the shenanigans.
                            
                            I’m looking forward to serving you.
                            
                            All the best,
                            
                            {your_first_name}
                            
                            P.S. Don’t give up now! Go to this link {page_url}.  I believe in you and want you to succeed.
                            
                            P.P.S.  If you haven’t already done so, I recommend that you sign up for my [blog, daily emails, FB group]. It’s 100% free and every week I pour my heart into giving you the most practical, usable information on {prod_name}.
                            
            
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
                        gr.Markdown("# Direct To Sales Page")
                        gr.Markdown("Generate a Email based on your inputs.")
                        
                        with gr.Row():
                            with gr.Column():
                                
                                
                                your_first_name = gr.Textbox(label="Add Your Name", value="John")                 
                                insert_problem = gr.Textbox(label="Tell About The Problem", value="finding your purpose")
                                desire = gr.Textbox(label="Add Your Desire Here", value=" true fulfillment")
                                cus_prob = gr.Textbox(label="Add Customer Problem Here" , value="discovering your purpose")
                                prod_name = gr.Textbox(label="Add Product Name" , value="PurposeFinder")             
                                page_url = gr.Textbox(label="Page URL" , value="www.yourwebsite.com/purposefinder")
                                tone=gr.Dropdown(choices=["Formal"," Informal","Friendly","Diplomatic","Inspirational"],label="Tone of the Email" , allow_custom_value=True ,value="Formal")
                                
                        with gr.Column():
                                btn = gr.Button("Generate Email")
                                output = gr.HTML(label="Generated Email")
                                
                        
                        btn.click(fn=generate_press_release, 
                                inputs=[your_first_name, insert_problem, desire, cus_prob, prod_name, page_url,tone], 
                                outputs=output)

        with gr.Tab("Email Template 2"):
                openai.api_key = key
                    #, benefits , unique_selling_point , pain_point , emotion
                    # Function to generate a press release based on user inputs
                with gr.Column():
                        def generate_press_release(web_name, your_name, start, sub_line,tone):
                            try:
                                # Save input data in a dictionary
                                input_data = {
                
                                    'web_name': web_name,
                                    'your_name': your_name,
                                    'start':start,
                                    'sub_line':sub_line,
                                    'tone': tone
                                    
                                    
                                }
                        
                                # Convert input data to a JSON string
                                input_data_json = json.dumps(input_data)
                        
                                # Define the template with placeholders for user inputs
                                prompt_text = f"""
                                Imagine you are a skilled public relations expert with years of experience in creating captivating emails that generate interest and coverage. You have been tasked with writing an email for:
                                {input_data_json}
                                
                                Subject Line: {web_name} Ch. 1 of 5
                                Condition: Everyone
                                Delay: Immediately
                                Body:
                
                                Hey, this is {your_name}, and I want to “officially” welcome you into my world :-)
                
                                {start}
                
                                {web_name} is where I share what I’ve learned.
                
                                My goal is to give away better stuff for FREE than most people charge for.
                
                                In fact, tomorrow I’m going to do just that. I’m going to let you go through one of my best products for FREE… and you ONLY pay me if you think it’s worth it… but ONLY if you open the email when it comes.
                
                                Yep, you heard me right…
                
                                I want our relationship to start out great…
                
                                So I’m going to WOW you with SO much value that you’ll feel obligated to buy stuff from me in the future (just kidding… kinda.)
                
                                Sound good?
                
                                Cool… then look for my email tomorrow.
                                Thanks,
                                {your_name}
                
                                P.S. The subject line is “{sub_line}” --so look for it!
                
                                
                
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
                            gr.Markdown("# SOAP OPERA SEQUENCE")
                            gr.Markdown("Generate a Email based on your inputs.")
                            
                            with gr.Row():
                                with gr.Column():
                                    
                                    
                                    web_name = gr.Textbox(label="Web Site Name", value="ExampleWeb")                 
                                    your_name = gr.Textbox(label="Add Your Name", value="John Doe")
                                    start = gr.Textbox(label="How You Got Started", value="Welcome to my journey!")
                                    sub_line = gr.Textbox(label="Add Your Subline Here" , value="Free Access to My Best Product Tomorrow")
                                    tone=gr.Dropdown(choices=["Formal"," Informal","Friendly","Diplomatic","Inspirational"],label="Tone of the Email" , allow_custom_value=True ,value="Formal")
                                    
                            with gr.Column():
                                    btn = gr.Button("Generate Email")
                                    output = gr.HTML(label="Generated Email")
                                    
                            
                            btn.click(fn=generate_press_release, 
                                    inputs=[web_name,your_name, start, sub_line,tone], 
                                    outputs=output)
                            

        with gr.Tab("Email Template 3"):
            #gr.Column()
            openai.api_key = key
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
                        
                                Conclude the email by expressing {story} gratitude for the recipient's support and interest, and mention that more updates about {event} will be shared in the future.
                        
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
                                    
                                    
                                    event = gr.Textbox(label="Add event details", value="Annual Innovation Showcase")
                                    #product= gr.Dropdown(choices=["Children's Reading Book","Book Launch","Branding Services"],label="Service or Product Name" , allow_custom_value=True)
                                    #advantages= gr.Dropdown(choices=["Be the first to receive it","Collect your order", "Find the useful one"],label="Service or Product Advantages" , allow_custom_value=True)
                                    #benefits = gr.Dropdown(choices=["Can read","Motivational One","Can share with others"],label="Service or Product Benefits")
                                    story = gr.Textbox(label="Tell About Event Story", value="I wanted to share how excited we are about this event.")
                                    alert = gr.Textbox(label="Add important message over here", value="Must Get Ticket")
                                    name1 = gr.Textbox(label="Sender's Name" , value="Sara")
                                    #name1=gr.Dropdown(choices=["Johna","Jack","Thomas"],label="Recipient Name")
                                    name = gr.Textbox(label="Recipient Name" , value="Joseph")
                                    #name=gr.Dropdown(choices=["Anna","Joseph","John"],label="Sender's Name")
                                    tone=gr.Dropdown(choices=["Formal"," Informal","Friendly","Diplomatic","Inspirational"],label="Tone of the Email" , allow_custom_value=True ,value="Formal")
    
                            with gr.Column():
                                    btn = gr.Button("Generate Email")
                                    output = gr.HTML(label="Generated Email")
                                    
                            
                            btn.click(fn=generate_press_release, 
                                    inputs=[event,alert, story, 
                                            name1, name, tone], 
                                    outputs=output)

        with gr.Tab("Email Template 4"):


                        # Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
            openai.api_key = key
                            #, benefits , unique_selling_point , pain_point , emotion
                            # Function to generate a press release based on user inputs
            with gr.Column():
                    def generate_press_release(name, title, add1, add2, add3, link, tone):
                        try:
                            # Save input data in a dictionary
                            input_data = {
            
                                'name': name,
                                'title': title,
                                'add1': add1,
                                'add2':add2,
                                'add3': add3,
                                'link':link,
                                'tone': tone
                                
                                
                            }
                    
                            # Convert input data to a JSON string
                            input_data_json = json.dumps(input_data)
                    
                            # Define the template with placeholders for user inputs
                            prompt_text = f"""
                            Imagine you are a skilled public relations expert with years of experience in creating captivating emails that generate interest and coverage. You have been tasked with writing an email for:
                            {input_data_json}
                            
                            Subject: Thanks for joining us!
                            Hi {name}
                            Thanks for being part of my workshop on {title}
                            We’ve been really impressed with the feedback we’ve gotten.
                            It’s clear we struck a cord!
                            Here are few things people said
                            &quot;WOW! Sean You rocked me!!!!&quot;
                            &quot;Lets do it! love your passion&quot;
                            &quot;How does it get better than this????&quot;
                            &quot;Hell Yeah!!!! Sooo good&quot;
                            And I know that some of you had a hard time joining us LIVE so I wanted to make sure you had a chance to watch
                            the limited time replay in the FB group.
                            So for the next 72 hours you can go watch the full replay of TITLE by going HERE.
                            On this workshop we talked about:
                            ● {add1} eloborate this very deeply.
                            ● {add2} eloborate this very deeply.
                            ● {add3} eloborate this very deeply.
                            … and much more!
                            Go here to watch the replay for the next 72 hours
                            NAME
                            PS… there’s still time to grab a breakthrough session with me to help you  for 2022. Go here {link}
            
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
                        gr.Markdown("# SOAP OPERA SEQUENCE")
                        gr.Markdown("Generate a Email based on your inputs.")
                        
                        with gr.Row():
                            with gr.Column():
                                
                                
                                name = gr.Textbox(label="Name", value="Sarah")                 
                                title = gr.Textbox(label="Add The Title Name", value="Unlocking Your Potential")
                                add1 = gr.Textbox(label="Add what's Spoked Today Point 1", value="We explored the power of goal-setting and how it can transform your life.")
                                add2 = gr.Textbox(label="Add what's Spoked Today Point 2", value="We delved into effective time management strategies to boost productivity.")
                                add3 = gr.Textbox(label="Add what's Spoked Today Point 3", value="We discussed the importance of self-care and maintaining a healthy work-life balance.")
                                link = gr.Textbox(label="Add The Link To The Calender", value="www.yourwebsite.com/breakthrough-session")
                                tone=gr.Dropdown(choices=["Formal"," Informal","Friendly","Diplomatic","Inspirational"],label="Tone of the Email" , allow_custom_value=True ,value="Formal")
                                
                        with gr.Column():
                                btn = gr.Button("Generate Email")
                                output = gr.HTML(label="Generated Email")
                                
                        
                        btn.click(fn=generate_press_release, 
                                inputs=[name,title,add1,add2,add3,link,tone], 
                                outputs=output)

        with gr.Tab("Email Template 5"):

            openai.api_key = key

            with gr.Column():
                    def generate_press_release(subject, first_name, date, niche, benefit, event_title, add1, add2, add3, tone):
                        try:
                            # Save input data in a dictionary
                            input_data = {
            
                                'subject': subject,
                                'first_name': first_name,
                                'date': date,
                                'niche': niche,
                                'benefit': benefit,
                                'event_title': event_title,
                                'add1':add1,
                                'add2':add2,
                                'add3':add3,
                                'tone': tone       
                            }
                    
                            # Convert input data to a JSON string
                            input_data_json = json.dumps(input_data)
                    
                            # Define the template with placeholders for user inputs
                            prompt_text = f"""
                            Imagine you are a skilled public relations expert with years of experience in creating captivating emails that generate interest and coverage. You have been tasked with writing an email for:
                            {input_data_json}
                            
                            Subject: {subject}
                            Message:
                            Hi {first_name},
                            If you're in {niche}, this is an important email. Please read it right to the end.
                            SHORT VERSION:
                            I’m running a live online workshop on {date}, to help you have {benefit} the best year you've ever had in 2022. 
            
                            Click here to register.
            
                            FULL VERSION:
                            Imagine this: it's December 29th, feeling a challenging way and you're at the office, reading your emails. Everyone else has gone home, and you're still working. There's still so much stuff to do. 
                            You're trying to get it all done. 
                            Uhhh.... You worked hard this year. You're tired; exhausted even.
                            Where did the year go?
                            I don't know if you've ever felt that empty feeling, where you know you did okay. You worked so hard...but you don't have much to show for it.
                            That's why I’m writing to you right now...
                            See, right now, most [niche] are exhausted. Hanging on for a break.
                            You've done okay, kicked some of your goals - but not all of them.
                            You’re wondering: "How do I make next year different to this year?" 
                            As you look towards next year, I'm sure you hope that 2022's better. 
                            But hope is not enough. 
                            Without a solid plan in place, 2022 could be just another photocopy of this year.
                            But it doesn't have to be that way…
                            Instead of leaving the year exhausted, you can leave it excited.
                            Instead of leaving the year with not much to show for it, you can set yourself up for a new year full of purpose, productivity, and profit.
                            Instead of hoping that next year turns out better, you can be certain of it.
                            I want to help you make 2022 your best year ever...
                            That's why this {date}, I'm running a free online workshop called {event_title}.
                            In this fast-paced 90-minute training, you'll discover:
                            {add1} elaborate this deeply.
                            {add2} elaborate this deeply.
                            {add3} elaborate this deeply.
                            My life/business turned around when I learned these tactics.
                            Now, it's YOUR turn. 
                            REGISTER HERE.
                            Name
                            P.S. We only have 100 spaces on the workshop, so register now and get in early.
            
            
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
                        gr.Markdown("# SOAP OPERA SEQUENCE")
                        gr.Markdown("Generate a Email based on your inputs.")
                        
                        with gr.Row():
                            with gr.Column():
                                
                                
                                subject = gr.Textbox(label="Add Subject Over Here", value="Join Our Free Workshop: Transform Your 2022!")                 
                                first_name = gr.Textbox(label="Add Your Name", value=" Alex")
                                date = gr.Textbox(label="Add The Date", value="")
                                niche = gr.Textbox(label="Add Importatnt Quotes", value="Digital Marketing")
                                benefit = gr.Textbox(label="Add Benifits Here", value="your most successful and productive year ever")
                                event_title = gr.Textbox(label="Add Event Title Here ", value="2022 Mastery: Achieving Your Best Year Yet")
                                add1 = gr.Textbox(label="Add what's Spoked Today Point 1", value="Proven goal-setting strategies to achieve your biggest dreams.")
                                add2 = gr.Textbox(label="Add what's Spoked Today Point 2", value="Effective time management techniques for maximum productivity")
                                add3 = gr.Textbox(label="Add what's Spoked Today Point 3", value="Profit-boosting strategies to grow your business in 2022.")
                                tone=gr.Dropdown(choices=["Formal"," Informal","Friendly","Diplomatic","Inspirational"],label="Tone of the Email" , allow_custom_value=True ,value="Formal")
                                
                        with gr.Column():
                                btn = gr.Button("Generate Email")
                                output = gr.HTML(label="Generated Email")
                                
                        
                        btn.click(fn=generate_press_release, 
                                inputs=[subject, first_name, date, niche, benefit, event_title, add1, add2, add3, tone], 
                                outputs=output)  
    
    with gr.Accordion("Article Generation"):

            with gr.Tab("Article Generation"):
                # Define your OpenAI API key here
                openai_api_key = key

                def get_google_search_links(query, num_results=10):
                    try:
                        # Use the search function to fetch search results
                        results = list(search(query, num_results=num_results))
                        # Return only the first 'num_results' links
                        return results[:num_results]
                    except Exception as e:
                        print(f"An error occurred while fetching Google search results: {str(e)}")
                        return []
                    
                def load_html(search_links):
                    try:
                        loader = AsyncChromiumLoader(search_links)
                        html_list = loader.load()
                        bs_transformer = BeautifulSoupTransformer()
                        docs_transformed = bs_transformer.transform_documents(html_list,tags_to_extract=["span"])
                        text_list = [docs.page_content[0:200] for docs in docs_transformed]
                        return text_list
                    except:
                        pass
                        return []
                
                
                def langchain_function(prompt):
                    # Create the ChatOpenAI instance
                    chat_model = ChatOpenAI(
                        temperature=0,
                        openai_api_key=openai_api_key,
                        model_name="gpt-3.5-turbo")
                
                    # Set the prompt and create a list of messages
                    messages = [HumanMessage(content=prompt)]
                
                    # Get the model's response
                    edited_output = chat_model.predict_messages(messages)
                
                    # Wrap the edited text to a specific width
                    wrapped_edited_text = textwrap.fill(edited_output.content, width=80)
                
                    return wrapped_edited_text  # Ensure to return the result
                
                # Define a function to take user input and call langchain_function
                def generate_article(text_list, query):
                    prompt =  f"""
                                    Article Generating Prompt
                                    Imagine you are a seasoned technology journalist with a knack for unveiling the impacts of innovative breakthroughs on our daily lives. Your task is to generate an article that explores a groundbreaking technological advancement:
                                    Write the article using {text_list} and the {query}
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
                    result = langchain_function(prompt)
                    return result  # Ensure to return the result
                
                def main_function(query):
                    # Get the first 10 search result links
                    search_links = get_google_search_links(query)
                
                    if search_links:
                        output = load_html(search_links)
                        result = generate_article(output, query)
                        return result
                    else:
                        return "No search results found."
                
                # Using Gradio Blocks to create the UI
                with gr.Blocks() as app:
                    gr.Markdown("# Article Generator")
                    gr.Markdown("### Enter a query and click **Generate** to create an article.")
                    
                    with gr.Column():
                        
                        inp_query = gr.Textbox(placeholder="Enter your query here...")   
                        with gr.Column():
                            btn_generate = gr.Button("Generate")
                            out_article = gr.HTML(placeholder="Generated article will appear here...")
                        
                    btn_generate.click(fn=main_function, inputs=inp_query, outputs=out_article)
                          

if __name__ == "__main__":
    demo.launch(share=True)
