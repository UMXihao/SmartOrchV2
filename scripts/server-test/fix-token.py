"""
start llama.cpp server
build/bin/llama-server -m ${model_path}

using llama-server to finish bench mark
"""

import requests
import time
from tqdm import tqdm
from datasets import load_dataset
import evaluate

url = "http://127.0.0.1:8080/completion"
headers = {"Content-Type": "application/json"}

ttft = 0
tpot = 0

n = 10
for i in range(n):
    # 构造输入文本
    input_text = '''The internet, a global network connecting billions of devices, has profoundly reshaped nearly every aspect of modern life. Its origins, however, are surprisingly modest.  The story begins in the Cold War era, with the U.S. Department of Defense’s Advanced Research Projects Agency (ARPA).  In 1969, ARPA created ARPANET, a project designed to enable researchers to share computer resources. This initial network connected just four universities: UCLA, Stanford Research Institute, UC Santa Barbara, and the University of Utah. The primary goal wasn’t about cat videos or social media – it was about creating a decentralized communication system that could withstand a potential Soviet attack.  If one part of the network went down, others would remain operational.

Throughout the 1970s, ARPANET evolved, with the development of crucial protocols like TCP/IP (Transmission Control Protocol/Internet Protocol), which became the standard for communication over the network.  Email also emerged as a key application, fundamentally changing how people communicated professionally and personally.  However, access remained largely limited to academic and governmental institutions.

The 1980s saw the transition from ARPANET to the modern internet.  The National Science Foundation (NSF) played a crucial role, establishing NSFNET, a high-speed network connecting supercomputer centers across the United States. This significantly expanded network capacity and accessibility.  Crucially, NSFNET lifted restrictions on commercial traffic, paving the way for the internet’s commercialization.

The invention of the World Wide Web in 1989 by Tim Berners-Lee at CERN, the European Organization for Nuclear Research, was a watershed moment. Berners-Lee created the three fundamental technologies that underpin the Web: HTML (HyperText Markup Language), URL (Uniform Resource Locator), and HTTP (Hypertext Transfer Protocol). These allowed for the creation of interconnected documents and easily navigable information. The first web browser, WorldWideWeb (later renamed Nexus), was also developed.

The 1990s witnessed the explosive growth of the internet, fueled by the release of user-friendly browsers like Mosaic and Netscape Navigator.  The dot-com boom saw a surge of investment in internet-based companies, although many ultimately failed.  Despite the bubble burst, the underlying infrastructure and user base continued to expand rapidly.

Today, the internet is an integral part of global society. It facilitates communication, commerce, education, entertainment, and countless other activities.  Social media platforms connect billions of people worldwide, while e-commerce has revolutionized retail. The rise of mobile devices and wireless internet access has further extended the internet’s reach, making it accessible to an unprecedented number of people.

However, the internet also presents significant challenges. Concerns about privacy, security, misinformation, and digital inequality remain pressing issues. The future of the internet will likely involve ongoing debates about net neutrality, data governance, and the ethical implications of artificial intelligence.  Nevertheless, the internet's impact on humanity is undeniable and continues to unfold.'''

    data = {"prompt": input_text, "n_predict": 128, "stop": "\n", "cache_prompt": False}

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    prompt_ms = response.json().get("timings").get("prompt_ms")
    predicted_per_token_ms = response.json().get("timings").get("predicted_per_token_ms")
    ttft += prompt_ms
    tpot += predicted_per_token_ms
    print("TTFT: ", prompt_ms, " TPOT: ", predicted_per_token_ms)

print("Average TTFT: ", ttft/n)
print("Average TPOT: ", tpot/n)
