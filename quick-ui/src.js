const getResponse = document.getElementById('getResponse')

getResponse.addEventListener('click', () => {
    const es = new EventSource('http://localhost:5001/get-advice?mood=excited');

    es.onmessage = function(event) {
        alert(event.data)
    }
    es.onerror = function(error) {
        alert(JSON.stringify(error))
    }
})