async function uploadPDF(){

const fileInput = document.getElementById("pdfFile")

const formData = new FormData()

formData.append("file", fileInput.files[0])

await fetch("/upload",{
method:"POST",
body:formData
})

alert("PDF Uploaded Successfully")

}



async function askQuestion(){

const input = document.getElementById("questionInput")
const question = input.value

const chatBox = document.getElementById("chatBox")

chatBox.innerHTML += `<div class="message user"><b>You:</b> ${question}</div>`

input.value = ""

const response = await fetch("/ask",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({question:question})

})

const data = await response.json()

chatBox.innerHTML += `<div class="message bot"><b>Assistant:</b> ${data.answer}</div>`

chatBox.scrollTop = chatBox.scrollHeight

}