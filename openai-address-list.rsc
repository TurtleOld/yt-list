/ip firewall address-list
remove [find list=openai]
add list=openai address=104.18.32.0/24 comment="chatgpt.com"
add list=openai address=104.18.37.0/24 comment="chat.openai.com"
add list=openai address=104.18.41.0/24 comment="cdn.oaistatic.com,oaistatic.com"
add list=openai address=172.64.146.0/24 comment="cdn.oaistatic.com,oaistatic.com"
add list=openai address=172.64.150.0/24 comment="chat.openai.com"
add list=openai address=172.64.155.0/24 comment="chatgpt.com"
