function sendAccordionData() {
    var form = $('#accordion-create-form').serialize();

    return {
        url: '../accordion-config/',
        data: {
            'form': form,
        }
    }
}

function afterLoadPollConfigModal() {
    console.log("HUEHUEHUE");    
}