# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    gpt3.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: tgarriss <tgarriss@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/11/18 10:37:53 by tgarriss          #+#    #+#              #
#    Updated: 2021/11/18 11:43:01 by tgarriss         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import openai

openai.api_key = os.environ["OPENAI_KEY"]

def gpt3(prompt, engine='davinci', response_length=64,
			temperature=0.7, top_p=1, frequency_penalty=0,
			presence_penalty=0, start_text='', restart_text='', stop_seq=[]):
	response = openai.Completion.create(
		prompt=prompt + start_text,
		engine=engine,
		max_tokens=response_length,
		temperature=temperature,
		top_p=top_p,
		frequency_penalty=frequency_penalty,
		presence_penalty=presence_penalty,
		stop=stop_seq,
	)
	answer = response.choices[0]['text']
	new_prompt = prompt + start_text + answer + restart_text
	return answer, new_prompt

def chat():
	file = open("prompt.txt", "r")
	prompt = file.read()
	while True:
		prompt += input("WRONG: ")
		answer, prompt = gpt3(prompt,
							  temperature=0.9,
							  frequency_penalty=1,
							  presence_penalty=1,
							  start_text="\nRIGHT:",
							  restart_text="\nWRONG: ",
							  stop_seq=["\nWRONG:", "\n"],
		)
		print("GPT-3:" + answer)

if __name__ == '__main__':
	chat()