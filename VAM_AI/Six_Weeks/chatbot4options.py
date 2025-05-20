# suppress warnings
import warnings
import requests, os
import argparse
from PIL import Image
import gradio as gr
from together import Together
import textwrap
warnings.filterwarnings("ignore")

## FUNCTION 1: This Allows Us to Prompt the AI MODEL
# -------------------------------------------------
def prompt_llm(prompt, with_linebreak=False):
    # This function allows us to prompt an LLM via the Together API

    # model
    model = "meta-llama/Meta-Llama-3-8B-Instruct-Lite"

    # Calculate the number of tokens
    tokens = len(prompt.split())

    # Make the API call
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    output = response.choices[0].message.content

    if with_linebreak:
        # Wrap the output
        wrapped_output = textwrap.fill(output, width=50)

        return wrapped_output
    else:
        return output


## FUNCTION 2: This Allows Us to Generate Images
# -------------------------------------------------
def gen_image(prompt, width=256, height=256):
    # This function allows us to generate images from a prompt
    response = client.images.generate(
        prompt=prompt,
        model="black-forest-labs/FLUX.1-schnell-Free",  # Using a supported model
        steps=2,
        n=1,
    )
    image_url = response.data[0].url
    image_filename = "image.png"

    # Download the image using requests instead of wget
    response = requests.get(image_url)
    with open(image_filename, "wb") as f:
        f.write(response.content)
    img = Image.open(image_filename)
    img = img.resize((height, width))

    return img


## Function 3: This Allows Us to Create a Chatbot
# -------------------------------------------------
def bot_response_function(user_message, chat_history):
    # 1. YOUR CODE HERE - Add your external knowledge here
    external_knowledge = """
    Mathematics using numbers, patterns, and logical reasoning.
    """

    # 2. YOUR CODE HERE -  Give the LLM a prompt to respond to the user
    chatbot_prompt = f"""
    You are an old, eccentric, and very happy mathematician who loves solving complex equations.

    respond to this {user_message} following these instructions:

    ## Instructions:
    * be very concise
    * always try figure it out a way to use mathematics in your answer
    * use some emojis to make it more fun
    * Ground all your answers based on this external_knowledge {external_knowledge} use a friendly tone
    """

    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3-8B-Instruct-Lite",
        messages=[{"role": "user", "content": chatbot_prompt}],
    )
    response = response.choices[0].message.content

    # 3. YOUR CODE HERE - Generate image based on the response
    #image_prompt = f"A {response} in a pop art style"
    #image = gen_image(image_prompt)
    from PIL import Image
    image = Image.open("results/image_option_2.png")

    # Append the response and image to the chat history
    chat_history.append((user_message, response))
    return "", chat_history, image


if __name__ == "__main__":
    # args on which to run the script
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--option", type=int, default=1)
    parser.add_argument("-k", "--api_key", type=str, default=None)
    args = parser.parse_args()

    # Get Client for your LLMs
    client = Together(api_key=args.api_key)

    # run the script
    if args.option == 1:
        ### Task 1: YOUR CODE HERE - Write a prompt for the LLM to respond to the user
        prompt = "write about Vancouver Canada"

        # Get Response
        response = prompt_llm(prompt)

        print("\nResponse:\n")
        print(response)
        print("-" * 100)

    elif args.option == 2:
        ### Task 2: YOUR CODE HERE - Write a prompt for the LLM to generate an image
        prompt = "Create an image of an old mathematician who looks a bit crazy but he has a big smile on his face"

        print(f"\nCreating Image for your prompt: {prompt} ")
        img = gen_image(prompt=prompt, width=256, height=256)
        os.makedirs("results", exist_ok=True)
        img.save("results/image_option_2.png")
        print("\nImage saved to results/image_option_2.png\n")

    elif args.option == 3:
        ### Task 3: YOUR CODE HERE - Write a prompt for the LLM to generate text and an image
        text_prompt = "write a 2 line post about AI and chatbots in Vancouver for instagram"
        image_prompt = f"give me an image that represents this '{text_prompt}'"

        # Generate Text
        response = prompt_llm(text_prompt, with_linebreak=True)

        print("\nResponse:\n")
        print(response)
        print("-" * 100)

        # Generate Image
        print(f"\nCreating Image for your prompt: {image_prompt}... ")
        img = gen_image(prompt=image_prompt, width=256, height=256)
        img.save("results/image_option_3.png")
        print("\nImage saved to results/image_option_3.png\n")

    elif args.option == 4:
        # 4. Task 4: Create the chatbot interface (see bot_response_function for more details)
        with gr.Blocks(theme=gr.themes.Soft()) as app:
            gr.Markdown("## 🤖 AI Chatbot")
            gr.Markdown("Enter your message below and let the chatbot respond!")

            chatbot = gr.Chatbot()
            #image_output = gr.Image(label="Generated Image")
            image_output = gr.Image(value="results/image_option_2.png", label="Generated Image")


            user_input = gr.Textbox(
                placeholder="Type your message here...", label="Your Message"
            )
            send_button = gr.Button("Send")

            send_button.click(
                bot_response_function,
                inputs=[user_input, chatbot],
                outputs=[user_input, chatbot, image_output],
            )
            user_input.submit(
                bot_response_function,
                inputs=[user_input, chatbot],
                outputs=[user_input, chatbot, image_output],
            )

        app.launch()
    else:
        print("Invalid option")