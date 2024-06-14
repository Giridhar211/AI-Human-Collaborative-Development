from onvif import ONVIFCamera
from onvif.exceptions import ONVIFError


def get_camera_info(camera_ip, username, password):
    try:
        camera = ONVIFCamera(camera_ip, 80, username, password)

        # Step 2: Discover the camera services
        media_service = camera.create_media_service()
        device_service = camera.create_devicemgmt_service()
        # Step 3: Retrieve device information
        device_info = device_service.GetDeviceInformation()
        manufacturer = device_info.Manufacturer
        model = device_info.Model
        firmware_version = device_info.FirmwareVersion
        serial_number = device_info.SerialNumber

        # Step 4: Fetch available profiles
        profiles = media_service.GetProfiles()

        # Step 5: Obtain stream URI for a profile
        profile_token = profiles[0].token  # Assuming the first profile
        stream_uri = media_service.GetStreamUri(
            {'StreamSetup': {'Stream': 'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}},
             'ProfileToken': profile_token}
        ).Uri
        print({
            'manufacturer': manufacturer,
            'model': model,
            'firmware_version': firmware_version,
            'serial_number': serial_number,
            'stream_uri': stream_uri
        })
        return {
            'manufacturer': manufacturer,
            'model': model,
            'firmware_version': firmware_version,
            'serial_number': serial_number,
            'stream_uri': stream_uri
        }
    except ONVIFError as  e:
        print(f'Error connecting to the camera: {e}')


if __name__ == "__main__":
    get_camera_info("192.168.29.198", "admin", "12345")