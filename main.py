from VideoDetect import*
videoTest = VideoDetect()
print(videoTest.detect_video("cVEemOmHw9Y"))
print(videoTest.detect_video("u9GNf51_NvU"))

print(videoTest.get_popularVal(channel = "Apple"))
print(videoTest.get_last_info())
print(videoTest.get_channel_info("Apple"))