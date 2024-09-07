import asyncio
import socket

from PIL import Image

from winrt.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager

from winrt.windows.storage.streams import \
    DataReader, Buffer, InputStreamOptions

async def get_media_info_async():
    sessions = await MediaManager.request_async()

    current_session = sessions.get_current_session()
    if current_session:
        if current_session.source_app_user_model_id == current_session.source_app_user_model_id:
            info = await current_session.try_get_media_properties_async()

            info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}

            info_dict['genres'] = list(info_dict['genres'])
            player = str(current_session.source_app_user_model_id).lower()

            del info_dict['genres']
            del info_dict['subtitle']
            del info_dict['playback_type']

            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('1.1.1.1', 0))

            info_dict['cover'] = f'http://{s.getsockname()[0]}:3162/cover'

            if player.lower().endswith('.exe'):
                player = player[:-4]

            info_dict['player'] = player

            return info_dict

    raise Exception('TARGET_PROGRAM is not the current media session')

def crop_image(image_path):
    # Open the image
    img = Image.open(image_path).convert("RGBA")

    # Initialize variables
    left, top, right, bottom = img.size[0], img.size[1], 0, 0

    # Get the image data
    data = img.getdata()

    # Loop through each pixel to find non-transparent bounding box
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            # Get the RGBA value of the pixel
            r, g, b, a = data[x + y * img.size[0]]
            if a > 0:  # Check if the pixel is not transparent
                if x < left:
                    left = x
                if x > right:
                    right = x
                if y < top:
                    top = y
                if y > bottom:
                    bottom = y

    # Check if we have non-transparent pixels
    if left > right or top > bottom:
        # Image is fully transparent
        return

    # Crop image to the bounding box
    img = img.crop((left + 1, top + 1, right, 233))

    # Save the cropped image (overwrite the original file)
    img.save(image_path)

async def read_stream_into_buffer(stream_ref, buffer):
    readable_stream = await stream_ref.open_read_async()
    readable_stream.read_async(buffer, buffer.capacity, InputStreamOptions.READ_AHEAD)

def get_media_thumbnail():
    media_info = asyncio.run(get_media_info_async())

    thumb_stream_ref = media_info['thumbnail']

    thumb_read_buffer = Buffer(5000000)

    asyncio.run(read_stream_into_buffer(thumb_stream_ref, thumb_read_buffer))

    buffer_reader = DataReader.from_buffer(thumb_read_buffer)
    byte_buffer = buffer_reader.read_bytes(thumb_read_buffer.length)

    filename = '../../../thumb_cache.png'

    with open(filename, 'wb+') as fobj:
        fobj.write(bytearray(byte_buffer))

    crop_image(filename)

    return filename