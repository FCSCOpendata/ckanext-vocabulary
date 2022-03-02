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
          <input type="text" name="ar" class="form-control" required>
        </div>
      </div>
      `
    )
    let htmlLength = $('#tags .form-row').toArray().length
    
    if (htmlLength > 2) {
      $('#rtag').show()
    }
    
  })

  $('#rtag').click((e) => {
    let html = $('#tags .form-row').toArray()
    html = html.slice(0, html.length -1)
    $('#tags').html(html)

    if( html.length <=2 ) {
      $('#rtag').hide()
    }
  })
})