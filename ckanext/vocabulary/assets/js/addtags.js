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
  })
})