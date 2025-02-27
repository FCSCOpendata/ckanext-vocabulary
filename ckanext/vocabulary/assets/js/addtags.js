$(document).ready(()=> {

  $('#adtag').click((e) => {
    e.preventDefault()

    $('#tags').append(
      `
      <div class="form-row">
        <div class="form-group col-md-6">
          <input type="text" name="en" class="form-control" >
        </div>
        <div class="form-group col-md-6">
          <input type="text" name="ar" class="form-control" dir="rtl" required>
        </div>
      </div>
      `
    )
    let htmlLength = $('#tags .form-row').toArray().length
    
    if (htmlLength > 1) {
      $('#rtag').css('visibility', 'visible');
    }
    
  })

  $('#rtag').click((e) => {
    let html = $('#tags .form-row').toArray()
    html = html.slice(0, html.length -1)
    $('#tags').html(html)

    if( html.length <=1 ) {
      $('#rtag').css('visibility', 'hidden');
    }
  })
})