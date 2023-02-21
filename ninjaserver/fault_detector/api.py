from ninja import NinjaAPI, File, Schema
from ninja.files import UploadedFile
from typing import List

from fault_detector.models import EventSignal
from fault_detector.schema import SignalNameSchema, EventSignalSchema, NotFoundSchema
# Custom Package
from utils_tesis.signalload import CSV_pandas_path
import utils_tesis.plot_api as plt_api

import shutil
import os
import glob

api =NinjaAPI()
print(os.getcwd())
temp_csv_path = f"{os.getcwd()}/fault_detector/temp_csv"
if not os.path.isdir(temp_csv_path):
    print('Creating temp csv folder')
    os.makedirs(temp_csv_path)
else:
    print('Deleting Existing files')
    file_list = glob.glob(f"{temp_csv_path}/*.csv")
    for file in file_list:
        os.remove(file)

# Variables
request_information = {}

def newRequest(csv_file_path, csv_file_name):
    request_information.clear()
    signals = CSV_pandas_path(csv_file_path)
    request_information["plots"] = {}
    request_information["signals"] = signals
    request_information["window_length"] = 64
    request_information["step"] = 4
    request_information["filename"] = csv_file_name
    return {"signals_list": signals.labels_list, "file_name": csv_file_name}

@api.post('/uploadCSV', tags=['CSV'])
def post_CSV(request, csv_files: UploadedFile = File(...)):
    csv_file_path = f"{temp_csv_path}/{csv_files.name}"
    
    with open(csv_file_path, "wb+") as f:
        f.write(csv_files.file.read())
    csv_file_name = csv_files.name
    
    

    print(f"csv filename: {csv_file_name}")
    
    response = newRequest(csv_file_path, csv_file_name)
    return response

@api.get('/csvSampleSelect/{id}', tags=['CSV'])
def get_sample_csv(request, id: int):
    try:
        csv_file = EventSignal.objects.get(pk=id)
        csv_file_path = str(csv_file.CSV)
        print(csv_file_path)
        csv_file_name = str(csv_file.title)
        response = newRequest(csv_file_path, csv_file_name)
        return response
    except:
        return {'Error': 'Blank space in Dropdown'}
    

    
@api.post("/signalName", tags=["CSV"])
def post_signal_name(request, load: SignalNameSchema):
    signal_name = load.signal_name
    
    # Update signal information
    request_information.pop('signal', None)
    request_information.pop('si_signal', None)
    request_information.pop('signal_windows', None)
    request_information.pop('si_signal_windows', None)
    request_information.pop('fft_windows', None)
    request_information.pop('si_fft_windows', None)
    request_information.pop('trip_windows', None)
    request_information.pop('si_trip_windows', None)

    request_information["signal_name"] = signal_name

    return {"response": signal_name}

# Static Plots

@api.get("/plots/imgSignal", tags=["static_plots"])
def plot_signal(request):
    t, signal, line_shape, plot_type = plt_api.img_signal(request_information)
    print(plot_type)
    return [t, signal, line_shape, plot_type]

@api.get("/plots/imgSISignal", tags=["static_plots"])
def plot_si_signal(request):
    # print(f"Request: {request.body.decode() }")
    t, si_signal, line_shape, plot_type = plt_api.img_si_signal(request_information)
    print(plot_type)
    return [t, si_signal, line_shape, plot_type]

@api.get("/plots/imgTrip", tags=["static_plots"])
def plot_trip_signal(request):

    t_window, trip, line_shape, plot_type = plt_api.img_trip(request_information)
    print(plot_type)
    return [t_window, trip, line_shape, plot_type]

@api.get("/plots/imgSITrip", tags=["static_plots"])
def plot_trip_si_signal(request):

    t_window, trip, line_shape, plot_type = plt_api.img_si_trip(request_information)
    print(plot_type)
    return [t_window, trip, line_shape, plot_type]

# Animations

@api.get("/plots/animSignal", tags=["animations"])
def plot_signal_anim(request):
    t_windows, signal_windows, line_shape, plot_type = plt_api.anim_signal(
        request_information
    )

    return [t_windows, signal_windows, line_shape, plot_type]


@api.get("/plots/animSISignal", tags=["animations"])
async def plot_si_signal_anim(request):
    t_windows, si_signal_windows, line_shape, plot_type = plt_api.anim_si_signal(
        request_information
    )
    return [t_windows, si_signal_windows, line_shape, plot_type]


@api.get("/plots/animFFT", tags=["animatons"])
async def plot_fft_anim(request):
    xf, fft_windows, max_min, plot_type = plt_api.anim_fft(request_information)
    return [xf, fft_windows, max_min, plot_type]


@api.get("/plots/animSIFFT", tags=["animations"])
async def plot_si_fft_anim(request):
    xf, si_fft_windows, max_min, plot_type = plt_api.anim_si_fft(request_information)
    
    return [xf, si_fft_windows, max_min, plot_type]



@api.get("/csvSamples", response=List[EventSignalSchema])
def csvSamples(request):
        return EventSignal.objects.all()
         

@api.get('/csvSamples/{csv_id}', response={200: EventSignalSchema, 404: NotFoundSchema})
def csvSample(request, csv_id:int):
    try:
        csv_file = EventSignal.objects.get(pk=csv_id)
        print(csv_file.CSV)
        shutil.copy(str(csv_file.CSV), temp_csv_path)

        return 200, csv_file
    except EventSignal.DoesNotExist as e:
        return 404, {"message": "CSV not found"}

# app.mount("/", StaticFiles(directory="public", html=True), name="static")