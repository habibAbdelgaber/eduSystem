function removeAlertMessage(){
    const alertMessage = document.querySelector('#alertMessage')
  if(alertMessage){
alertMessage.style.display = 'none';
  }
}

setTimeout(removeAlertMessage, 5000) // dismiss alert message after 5 seconds

