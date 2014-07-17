var _validFileExtensions = [".jpg", ".jpeg", ".bmp", ".gif", ".png"];

function Validate(oForm) {
    var arrInputs = oForm.getElementsByTagName("input");
    for (var i = 0; i < arrInputs.length; i++) {
        var oInput = arrInputs[i];
        if (oInput.type == "file" && oInput.size) {
            var sFileName = oInput.value;
            if (sFileName.length > 0) {
                var blnValid = false;
                for (var j = 0; j < _validFileExtensions.length; j++) {
                    var sCurExtension = _validFileExtensions[j];
                    if (sFileName.substr(sFileName.length - sCurExtension.length, sCurExtension.length).toLowerCase() == sCurExtension.toLowerCase()) {
                        blnValid = true;
                        break;
                    }
                }
                if (!blnValid) {

                    return false;
                }
            }
        }
    }
    return true;
}

$('#id_imagen').bind('change', function () {
    if (this.files[0].size / 1024 / 1024 > 5) {
        $(this).val('');
        alert("Por favor ingrese un archivo con un peso maximo de 5 MB");
    }else{
    }
});

function validar(oForm) {
    if (Validate(oForm)) {
        return true;
    } else {
        return false;
    }
}
