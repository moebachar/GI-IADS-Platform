from models import YoloModel


def test_yolo_model():
    yolomodel = YoloModel(model_name="yolov8n.yaml", n_epochs=3, learning_rate= 0.01, batch_size=16)

    print('Donner votre instruction:\n 1. Pour entrainer le modeèle\n 2. Pour quitter\n')
    instruction = int(input())
    if instruction == 1:
        result = yolomodel.train_model()
        print(result)
        print('-----------------------------')
        print('Training model...')
        print('-----------------------------')
    elif instruction == 2:
        print('-----------------------------')
        print('Quitting...')
        print('-----------------------------')
    else:
        print('-----------------------------')
        print('Instruction invalide')
        print('-----------------------------')

    if yolomodel.training_complete:
        print('--------------------------------')
        print('Training complete')
        print('--------------------------------')
        print('--------------------------------')
        print('Plotting metrics...')
        print('--------------------------------')
        yolomodel.plot_metrics()
        if yolomodel.plot_complete:
            print('--------------------------------')
            print('Metrics plotted')
            print('--------------------------------')

            print('Choisir une manière de tester le modèle: \n 1. Pour tester sur une image \n 2. Pour tester avec la webcam \n 3. Pour quitter\n')
            instruction = int(input())
            if instruction == 1:
                print('--------------------------------')
                print('Testing on image...')
                print('--------------------------------')
                yolomodel.plot_results('jpg', r'C:\Users\dioud\Desktop\Projet_expertise\GIA-Platform\object_detection\model_with_streamlit\data\test\images\WhatsApp-Image-2022-06-14-at-9-55-12-PM--1-_jpeg.rf.52625e346939c02baba53fde6d6d94dd.jpg')
                print('--------------------------------')
                print('Tested on image')
                print('--------------------------------')
            elif instruction == 2:
                print('--------------------------------')
                print('Testing on webcam...')
                print('--------------------------------')
                yolomodel.predict_on_video(mode='webcam')
                print('--------------------------------')
                print('Tested on webcam')
                print('--------------------------------')
            elif instruction == 3:
                print('--------------------------------')
                print('Quitting...')
                print('--------------------------------')
            else:
                print('--------------------------------')
                print('Instruction invalide')
                print('--------------------------------')


test_yolo_model()
    



