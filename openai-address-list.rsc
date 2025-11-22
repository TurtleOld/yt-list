/ip firewall address-list
remove [find list=openai]
add list=openai address=162.159.140.245 comment="api.openai.com"
add list=openai address=172.66.0.243 comment="api.openai.com"
add list=openai address=104.18.37.228 comment="chat.openai.com"
add list=openai address=172.64.150.28 comment="chat.openai.com"
add list=openai address=104.18.32.47 comment="chatgpt.com"
add list=openai address=172.64.155.209 comment="chatgpt.com"
