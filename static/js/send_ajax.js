function sendAjax(obj){
  $.ajax({
    type: $(obj).attr('method'),
    url: $(obj).attr('action'),
    data: $(obj).serialize()
  })
  .done(function(data){
    if(data.success) {
      console.log(data.success);
      showMsg('#ajax-msg',data.msg);
    }
    else{
      showMsg('#ajax-msg-error',data.msg);    
    }

  })
  .fail(function( jqXHR, textStatus, errorThrown ){
    console.log(errorThrown);
    showMsg('#ajax-msg-error','Error: Ha ocurrido un problema de comunicación con el servidor.'); 
  })
  return false;
};