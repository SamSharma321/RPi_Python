import requests
import os


class DeepSeekAI():
    DS_API_KEY = os.getenv('DS_API_KEY', 'sk-bfe8e6258afc46ea88c748e464899258')
    DS_API_URL = 'https://api.deepseek.com/v1/chat/completions'  # Replace with actual API endpoint

    def process_request(self, input_text=None, mode=0):
        '''
        :brief: This function is used to process the API request for DeepSeekAI
        :param input_text:
        :return:
        '''
        headers = {
            'Authorization': f'Bearer {self.DS_API_KEY}',  # Replace with actual API key
            'Content-Type': 'application/json'}

        if mode == 1:
            input_text = 'Give a summarized result for ' + input_text

        # API Load for the API request - can be altered more
        payload = {
            'model': 'deepseek-chat',
            'messages': [
                {
                    'role': 'user',
                    'content': input_text   # Can be altered to make it more efficient
                }
            ],
            'max_tokens': 200 if mode == 1 else 400
        }

        # make the API request
        response = requests.post(self.DS_API_URL, headers=headers, json=payload)
        print(response)

        if response.status_code == 200: # Success  # 402 - payment required
            # Extract the response
            response_data = response.json()  # You get json as response
            processed_text = response_data['choices'][0]['message']['content']
            return processed_text
        else:
            return 'Sorry sir, I am not able to work to my full potential right now.'


if __name__ == '__main__':
    # Initialize DeepSeekAI
    deepseek = DeepSeekAI()

    # Process the request
    processed_text = deepseek.process_request('What is the capital of India?')
    print(processed_text)

    # Process the request
    processed_text = deepseek.process_request('What is the capital of India?', 1)
    print(processed_text)


