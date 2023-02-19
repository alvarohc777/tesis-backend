const playBtn = document.getElementById('play');
const stopBtn = document.getElementById('stop');
const plusSample = document.getElementById('plusSample');
const minusSample = document.getElementById('minusSample');
let playState = false;
let playIntervalID = 0;
let intervalId = 0;

// play button logic
playBtn.addEventListener('click', function () {
    // pause slider
    if (playState === true) {
        playState = false;
        clearInterval(playIntervalID)
        return
    };
    // restart slider when at end
    if (slider.value === slider.max) {
        slider.value = 0;

    }
    // play slider
    playState = true;
    playIntervalID = setInterval(playPlots, 70);
});

function playPlots() {
    if (playState === true) {
        slider.dispatchEvent(new Event('input', {}), slider.value++);
        if (slider.value === slider.max) {
            playState = false;
        }
    }
};


// stop button logic
stopBtn.addEventListener('click', function () {
    playState = false;
    clearInterval(playIntervalID);
    slider.dispatchEvent(new Event('input', {}), slider.value = 0);
});


// +1 button logic
plusSample.addEventListener('mousedown', function () {
    clearInterval(playIntervalID);
    playState = false;
    if (slider.value == slider.max) {
        slider.dispatchEvent(new Event('input', {}), slider.value = 0);
        return
    }
    slider.dispatchEvent(new Event('input', {}), slider.value++);

    intervalId = setInterval(() => {
        clearInterval(playIntervalID);
        slider.dispatchEvent(new Event('input', {}), slider.value++);
    }, 100);
})
plusSample.addEventListener('mouseup', () => { clearInterval(intervalId) })
plusSample.addEventListener('mouseout', () => { clearInterval(intervalId) })

// -1 button logic
minusSample.addEventListener('mousedown', function () {
    clearInterval(playIntervalID);
    playState = false;

    slider.dispatchEvent(new Event('input', {}), slider.value--);
    if (slider.value == 0) {
        slider.dispatchEvent(new Event('input', {}), slider.value = slider.max);
        return
    }
    intervalId = setInterval(() => {
        // slider.value--;
        slider.dispatchEvent(new Event('input', {}), slider.value--);
    }, 100);
})
minusSample.addEventListener('mouseup', () => { clearInterval(intervalId) })
minusSample.addEventListener('mouseout', () => { clearInterval(intervalId) })

// // Optional Behaviour: if slider moved, then animations is paused.
// slider.addEventListener('click', () => {
//     clearInterval(playIntervalID);
//     playState = false;
//     console.log('slider pressed')
// }) 