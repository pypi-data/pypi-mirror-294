import httpx

class ModelAI:
    def __init__(self):
        """
        Initializes a new instance of the ModelAI class.

        The __init__ method is a special method in Python that is automatically called when an object of the class is created.

        Parameters:
        - self: The instance of the class.

        Instance Variables:
        - self.url (str): The URL endpoint for making API requests.
        - self.headers (dict): The headers to be included in the HTTP request.

        Returns:
        - None
        """
        self.__url = 'https://gpt.thenduy.com/api/openai/v1/chat/completions'
        self.__headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.__payload = None
        self.__greeting = "This is AI for console, made by VUXNX."

    
    def prompt(self, command: str)->str:
        """
        Sends a prompt command to the GPT model and returns the generated response.

        The prompt method sends a POST request to the specified URL with the provided payload and headers.
        It expects a JSON response containing the generated response from the GPT model.

        Parameters:
        - self: The instance of the class.
        - command (str): The command or message to be sent to the GPT model.

        Returns:
        - str: The generated response from the GPT model.

        Raises:
        - Exception: If the HTTP request fails or returns a non-200 status code.
        """
        print(self.__greeting)
        self.__payload = {
            "model": "gpt-4o",
            "messages": [
                {"role": "user", "content": command}
            ],
            "stream": False,
            "temperature": 0.269,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "top_p": 1
        }

        try:
            with httpx.Client(http2=True) as client:

                response = client.post(self.__url, headers=self.__headers, json=self.__payload, cookies=None)
        
                if response.status_code == 200:
                    response_data = response.json()
                    return response_data['choices'][0]['message']['content']
                else:
                    raise Exception(f"Error: HTTP status code {response.status_code}")


        except Exception as e:
            print(f'Error: {e}')


if __name__ == '__main__':
    model = ModelAI()
    print(model.prompt("How are u today"))