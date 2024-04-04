<!DOCTYPE html>
<html lang='cz'>
<head>
    <meta charset='utf-8'/>
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Astronavigační cvičení</title>
	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
	<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
	<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
</head>
<body>
	<div class="jumbotron text-center">
		<h1>Astronavigační cvičení</h1>
	</div>
	
	<div style="margin-left:1em;">
	
	<div id="step1">
	  <pre>%(step1)s</pre>
    </div>
	
	<div style="padding:1em;">
	<button class="btn btn-primary" type="button" data-toggle="collapse" data-target="#step2" aria-expanded="false" aria-controls="step2">
    Show Ho, GHA, LHA, and Dec
	</button>
	</div>
	<div class="collapse" id="step2">
	  <pre>%(step2)s</pre>
    </div>
	
	<div style="padding:1em;">
	<button class="btn btn-primary" type="button" data-toggle="collapse" data-target="#step3" aria-expanded="false" aria-controls="step3">
    Show Hc, Zn, and real Lat, Lon
  </button>
  </div>
	<div class="collapse" id="step3">
	  <pre>%(step3)s</pre>
    </div>
	
	</div>
	
	<footer class="bg-light text-center text-lg-start">
		<div class="text-center p-3" style="background-color: rgba(0, 0, 0, 0.2);">
    &copy; <script>
    document.write(new Date().getFullYear());
</script> 
    <a class="text-dark" href="https://www.chovanec.com/">www.chovanec.com</a>
  </div>
	</footer>
</body>
</html>
