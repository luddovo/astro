<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
	<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
	<title>LAN Finder From A Series Of Measurements</title>
	<style>
		body {
			max-width: 800px;
			margin: 0 auto;
		}

	</style>
	<script>
		$(document).ready(setup)

		function setup() {
			// get rid of GET parameters
			window.history.replaceState({}, '', window.location.href.split('?')[0]);

			// set up validation
			$('#form').on('submit', function(e){
				var re = new RegExp(/^(\d{2}:\d{2}:\d{2}\s+\d+\-\d+(\.\d+)?)$/);
				var data = $('#data').val().trim()
				var lines = data.split('\n')
				var pass = 1
				for (var i = 0; i < lines.length; i++) {
					if (!re.test(lines[i].trim())) {
						pass = 0;
						break
					}
				}
				if (pass == 0) {
					e.preventDefault();
					alert('Invalid data');
				}
			});
				}
	</script>
	<link rel="icon" href="./favicon.ico" type="image/x-icon">
</head>

<body>
	<main>
		<div class="mb-4 p-3 bg-primary text-white rounded text-center">
			<h1>LAN Finder From A Series Of Measurements</h1>
		</div>
		<form id="form">
			<div class="form-group container">
				<div class="form-group row">
					<label for="lat" class="col-4 col-form-label">List Of Measurements<br>Example:<br>
						11:43:26 34-51<br>
						11:48:26 35-51<br>
						12:01:34 36-18<br>
						12:18:20 35-06<br>
					</label>
					<div class="col-8">
						<textarea id="data" name="data" rows="10" cols="20">%(data)s</textarea>
					</div>
				</div>

			<div class="text-center">
				<button type="submit" class="btn btn-primary" name="submit" value="submit">Get Hs</button>
			</div>
			</div>
		</form>
		<div class="mb-4 p-5 text-center">
			<h1 class="display-1 fw-bold">%(result)s</h1>
		</div>
		<div class="text-center" id="chart">
			%(chart)s
		</div>

	</main>
	<footer class="bg-light text-center text-lg-start">
    &copy; <script>
    document.write(new Date().getFullYear());
</script> 
    <a class="text-dark" href="https://www.chovanec.com/">www.chovanec.com</a>
	</footer>
</body>

</html>
