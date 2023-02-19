from ninja import NinjaAPI, File, Schema
from ninja.files import UploadedFile



from utils_tesis.signalload import CSV_pandas_path
import utils_tesis.plot_api as plt_api
from pydantic import BaseModel

api =NinjaAPI()

# class SignalName(BaseModel):
#     # csv_name: str
#     signal_name: str
class SignalName(Schema):
    # csv_name: str
    signal_name: str

@api.get('/hello')
def hello(request):
    return "Hello World"

# Variables
request_information = {}

@api.post('/uploadCSV', tags=['CSV'])
def post_CSV(request, csv_files: UploadedFile = File(...)):
    with open(csv_files.name, "wb+") as f:
        f.write(csv_files.file.read())
    request_information.clear()
    request_information["plots"] = {}
    csv_file_name = csv_files.name
    signals = CSV_pandas_path(csv_file_name)

    request_information["filename"] = csv_file_name
    request_information["signals"] = signals
    request_information["window_length"] = 64
    request_information["step"] = 4

    print(f"csv filename: {csv_file_name}")

    return {"signals_list": signals.labels_list, "file_name": csv_file_name}

    
@api.post("/signalName", tags=["CSV"])
def post_signal_name(request, load: SignalName):
    signal_name = load.signal_name
    # signals = request_information["signals"]
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

@api.post("/plots/imgSITrip", tags=["static_plots"])
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

# app.mount("/", StaticFiles(directory="public", html=True), name="static")