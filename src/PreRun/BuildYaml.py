import os

yaml = f"""
server: # REST and WS server
  port: 2333
  address: 0.0.0.0

lavalink:
  server:
    password: "{os.getenv("LAVALINK_PSW")}"
    playerUpdateInterval: 5 # How frequently to send player updates to clients, in seconds
    statsTaskInterval: 60 # How frequently to send the node stats to clients, in seconds
    koe:
      useEpoll: true
      highPacketPriority: true
      bufferDurationMs: 400
      byteBufAllocator: "default"
    sources:
      # Remote sources
      bandcamp: true
      getyarn: true
      http: true
      odysee: true
      reddit: true
      soundcloud: true
      tiktok: true
      twitch: true
      vimeo: true
      yandex: true
      youtube: true

      # Local source
      local: false
    lavaplayer:
      nonAllocating: false # Whether to use the non-allocating frame buffer.
      frameBufferDuration: 5000 # The frame buffer duration, in milliseconds
      youtubePlaylistLoadLimit: 6 # Number of pages at 100 each
      gc-warnings: true
      youtubeSearchEnabled: true
      odyseeSearchEnabled: true
      soundcloudSearchEnabled: true
      yandexMusicSearchEnabled: true
      #youtubeConfig: (Youtube account credentials, needed to play age restricted tracks)
        #email: ""
        #password: ""
      # You can get your yandex oauth token here https://music-yandex-bot.ru/ used to remove the 30s limit on some tracks
      #yandexOAuthToken:
      #ratelimit:
        #ipBlocks: ["1.0.0.0/8", "..."] # list of ip blocks
        #excludedIps: ["...", "..."] # ips which should be explicit excluded from usage by lavalink
        #strategy: "RotateOnBan" # RotateOnBan | LoadBalance | NanoSwitch | RotatingNanoSwitch
        #searchTriggersFail: true # Whether a search 429 should trigger marking the ip as failing
        #retryLimit: -1 # -1 = use default lavaplayer value | 0 = infinity | >0 = retry will happen this numbers times

metrics:
  prometheus:
    enabled: true
    endpoint: /metrics

sentry:
  dsn: ""
  environment: ""
#  tags:
#    some_key: some_value
#    another_key: another_value

logging:
  file:
    path: ./logs/
  logback:
    rollingpolicy:
      max-file-size: 1GB
      max-history: 30

  level:
    root: INFO
    lavalink: INFO


"""



with open("./application.yml", "w") as f:
    f.writelines(yaml)