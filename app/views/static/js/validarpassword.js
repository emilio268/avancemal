function validarpassword(Usua_Pass) {
    const decimal = /^(?=.*\d)(?=.*[a-z])(?=.*[^a-zA-Z0-9])(?!.*\s).{8,15}$/;

    if(password.value.match(decimal)) {

        alert("El password es seguro !"); 

    } else {

        alert("El password debe contener al menos una minúscula, mayúscula, número y un carácter especial. Y 8 carácteres como mínimo.")

    }


}