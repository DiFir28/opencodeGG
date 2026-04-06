# import time
# import threading
# import json
# import cv2
# import camera
# import SharedArray as sa
# from shared import therds_stop, process_stop, cap_resolution
# from CVobj import CVobj, fieldimg, CVobj_threads, out_check
# from geometry import vec, point, sign, tup
# import numpy as np
# import theard_serial

# with open('borders.json', 'r', encoding='utf-8') as file:
#      borders = json.load(file)

# camera.process.start()
# time.sleep(1)



# read_thread = threading.Thread(target=theard_serial.read_from_arduino)
# read_thread.daemon = True
# read_thread.start()




# if  __name__ == "__main__":
#     try:
        
#         while True:
#             fr = camera.current_frame.copy()
#             # cut =int( ( cap_resolution[0] - cap_resolution[1] )/2)
#             # fr2 = fr[:,cut:(cut+cap_resolution[1])]
#             # fr3 = fr[cut:(cut+cap_resolution[1])][:]
#             #fr = cv2.resize(fr, (800,600))
#             # ball.sect = fr
#             # ball.calcang()
#             #theard_serial.write_to_arduino(f',{0},{0},{0},{0},{10},')

            
#             #cv2.imshow("ww", fr )
#             print(out_check(fr, borders["green"]["glob"]))
#             cv2.imshow("fr",  cv2.resize(fr, None, fx=0.5, fy=0.5) )
            
#             # cv2.imshow("fr2",cv2.resize(fr2, None, fx=0.5, fy=0.5)  )
#             # cv2.imshow("fr3",cv2.resize(fr3, None, fx=0.5, fy=0.5) )
#             #print(theard_serial.data)
           
#             time.sleep(0.01)
#             ch = cv2.waitKey(5)
#             if ch == 27:
#                 break
        
#     except KeyboardInterrupt:
#         print("\nПрограмма завершена")
#     finally:
#         print("Ending...")
#         process_stop.set()
#         therds_stop.set()
#         camera.process.join()
        
#         time.sleep(0.1)
#         cv2.destroyAllWindows()
#         print("End")


from picamera2 import Picamera2
import cv2

# Инициализация камеры
picam2 = Picamera2()

# Создаем конфигурацию (БЕЗ указания flip здесь)
config = picam2.create_preview_configuration(
    main={"format": "BGR888", "size": (1920, 1080)},
    raw={"size": picam2.sensor_resolution}
)

# Применяем конфигурацию
picam2.configure(config)

# Настройка отражения ПОСЛЕ configure()
picam2.set_controls({"Transform": {"hflip": True, "vflip": False}})  # ← Вот правильный способ!

# Запускаем камеру
picam2.start()

try:
    while True:
        # Захватываем кадр
        frame = picam2.capture_array()
        
        # Конвертация BGR -> RGB (если нужно)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Показываем изображение
        cv2.imshow("Mirrored Preview", frame_rgb)
        
        # Выход по 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Останавливаем камеру
    picam2.stop()
    cv2.destroyAllWindows()
