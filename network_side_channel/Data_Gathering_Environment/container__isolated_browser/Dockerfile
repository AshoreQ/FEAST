FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y vnc4server jwm firefox
RUN apt-get install -y tcpdump

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tshark

RUN apt-get install -y nano
RUN apt-get install -y python
RUN apt-get install -y python-scapy
RUN apt-get install -y mitmproxy
RUN apt-get install -y xautomation
RUN apt-get install -y python-flask
RUN apt-get install -y python-jinja2

ADD startup_script.sh /startup_script.sh
RUN chmod +x /startup_script.sh

ADD mypass /mypass

ADD capture_command.sh /capture_command.sh
RUN chmod +x /capture_command.sh

ADD trump_clinton_sanders_bookmarks.html /trump_clinton_sanders_bookmarks.html


ADD automate_istandwith_browser_hillary_donald.sh /automate_istandwith_browser_hillary_donald.sh
RUN chmod +x /automate_istandwith_browser_hillary_donald.sh

ADD automate_google_search.sh /automate_google_search.sh
RUN chmod +x /automate_google_search.sh


RUN mkdir /ebay_shoppingcart
ADD shopping_cart_test/exploit_page_template.html /ebay_shoppingcart/exploit_page_template.html
ADD shopping_cart_test/jinja_render_exploitpage.py /ebay_shoppingcart/jinja_render_exploitpage.py
ADD shopping_cart_test/local_automate_popup_exploit.sh /ebay_shoppingcart/local_automate_popup_exploit.sh
RUN chmod u+x /ebay_shoppingcart/local_automate_popup_exploit.sh
ADD shopping_cart_test/bookmarklet__add_to_cart /ebay_shoppingcart/bookmarklet__add_to_cart
ADD shopping_cart_test/bookmarklet__click_exploit /ebay_shoppingcart/bookmarklet__click_exploit


# Update the image
RUN echo "random372259" # Change to break cache and cause update/upgrade
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install firefox

#Set environment variables
ENV DISPLAY :0

CMD ./startup_script.sh
