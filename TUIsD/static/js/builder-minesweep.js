function sendMinesweepData() {
    var form = $('#minesweep-create-form').serialize();

    return {
        url: '../minesweep-config/',
        data: {
            'form': form,
        }
    }
}

function afterLoadPollConfigModal() {
    console.log("HUEHUEHUE");    
}