console.log("hello world")

const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();  // Trim spaces
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

const video = document.getElementById('video-element')
const image = document.getElementById('img-element')
const captureBtn = document.getElementById('capture-btn')
const reloadBtn = document.getElementById('reload-btn')
const user_id = $('#user_id').val();
console.log("User ID in JavaScript:", user_id);

reloadBtn.addEventListener('click', e => {
window.location.reload()
})

if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            video.srcObject = stream
            const { height, width } = stream.getTracks()[0].getSettings()

            captureBtn.addEventListener('click', e => {
                e.preventDefault()
                captureBtn.classList.add('not-visible')
                const track = stream.getVideoTracks()[0]
                const imageCapture = new ImageCapture(track)
                console.log(imageCapture)

                imageCapture.takePhoto().then(blob => {
                    console.log("took photo:", blob)
                    console.log("Blob size:", blob.size);
                    const img = new Image(width, height)
                    img.src = URL.createObjectURL(blob)
                    image.appendChild(img)

                    video.classList.add('not-visible')

                    const reader = new FileReader()

                    reader.readAsDataURL(blob)
                    reader.onloadend = () => {
                        const base64data = reader.result
                        console.log(base64data)

                        const fd = new FormData()
                        fd.append('csrfmiddlewaretoken', csrftoken)
                        fd.append('photo', base64data)
                        fd.append('user_id', user_id);

                        console.log("fd:", fd)

                        $.ajax({
                            type: 'POST',
                            url: '/esign/classify/',
                            enctype: 'multipart/form-data',
                            data: fd,
                            processData: false,
                            contentType: false,
                            beforeSend: function (xhr) {
                                xhr.setRequestHeader('X-CSRFToken', csrftoken);  // Set CSRF token in headers
                            },
                            success: (resp) => {
                                console.log(resp)
                                if(resp.success) {
                                window.location.href = "/esign/home/"
                                }
                                else {
                                    alert("Error: " + resp.error);
                                }
                            },
                            error: (err) => {
                                console.log(err)
                            }
                        })
                    }
                }).catch(error => {
                    console.log("takePhoto() error:", error);
                });
            });
        })
        .catch(error => {
            console.log("Something went wrong!", error);
        })
}