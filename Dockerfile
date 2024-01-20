FROM openhab/openhab:latest

WORKDIR /openhab

COPY html/ /openhab/conf/html/
COPY icons/ /openhab/conf/icons/
COPY items/ /openhab/conf/items/
COPY persistence/ /openhab/conf/persistence/
COPY rules/ /openhab/conf/rules/
COPY scripts/ /openhab/conf/scripts/
COPY services/ /openhab/conf/services/
COPY sitemaps/ /openhab/conf/sitemaps/
COPY sounds/ /openhab/conf/sounds/
COPY things/ /openhab/conf/things/
COPY transform/ /openhab/conf/transform/
