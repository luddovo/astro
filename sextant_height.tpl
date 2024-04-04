<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
	<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
	<title>Sextant Height Calculator</title>
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

			// if lat, lon empty, prefill
			if ( !$("#lat").val() || !$("#lon").val() ) {
				if (navigator.geolocation) {
					navigator.geolocation.getCurrentPosition(positionFound, positionNotFound);
				}
			}

			// if date empty, prefill
			if ( !$("#date").val() ) {
				$("#date").val(new Date().toISOString().slice(0, 10))
			}

			// if time empty, prefill
			if ( !$("#time").val() ) {
				$("#time").val(new Date().toISOString().slice(11, 19))
			}

			// if no limb, select lower
			if (!$("#upper").prop('checked') && !$("#lower").prop('checked') && !$("#center").prop('checked')) {
				$("#lower").prop('checked', true)
			}

			// if eye_height empty, prefill
			if ( !$("#eye_height").val() ) {
				$("#eye_height").val(2)
			}
			
		}

		function positionFound(position) {
			$("#lat").val(position.coords.latitude)
			$("#lon").val(position.coords.longitude)
		}

		function positionNotFound(error) {
		}

	</script>
	<link rel="icon" href="./favicon.ico" type="image/x-icon">
</head>

<body>
	<main>
		<div class="mb-4 p-3 bg-primary text-white rounded text-center">
			<h1>Sextant Height Calculator (Sun)</h1>
		</div>
		<form>
			<div class="form-group container">
				<div class="form-group row">
					<label for="lat" class="col-4 col-form-label">Lat:</label>
					<div class="col-8">
						<input class="form-control" type="text" id="lat" name="lat" value="%(lat)s" required pattern="^[\-]?\d+(\.\d+)?\s*$"><br>
					</div>
				</div>

				<div class="form-group row">
					<label for="lon" class="col-4 col-form-label">Lon:</label>
					<div class="col-8">
						<input class="form-control" type="text" id="lon" name="lon" value="%(lon)s" required pattern="^[\-]?\d+(\.\d+)?\s*$"><br>
					</div>
				</div>

				<div class="form-group row">
					<label for="date" class="col-4 col-form-label">Date:</label>
					<div class="col-8">
						<input class="form-control" type="text" id="date" name="date" value="%(date)s" required pattern="^\d{4}-\d{2}-\d{2}\s*$"><br>
					</div>
				</div>

				<div class="form-group row">
					<label for="time" class="col-4 col-form-label">Time (UTC):</label>
					<div class="col-8">
						<input class="form-control" type="text" id="time" name="time" value="%(time)s" required pattern="^\d{2}:\d{2}:\d{2}\s*$"><br>
					</div>
				</div>

			<div class="container mb-4">
				<input type="radio" class="btn-check" name="limb" id="upper" value="upper" %(upper_checked)s>
				<label class="btn btn-outline-primary" for="upper">Upper Limb</label>
			  
				<input type="radio" class="btn-check" name="limb" id="lower" value="lower" %(lower_checked)s>
				<label class="btn btn-outline-primary" for="lower">Lower Limb</label>
			  
				<input type="radio" class="btn-check" name="limb" id="center" value="center" %(center_checked)s>
				<label class="btn btn-outline-primary" for="center">Center</label>
			</div>

			<div class="form-group row">
				<label for="eye_height" class="col-4 col-form-label">Eye Height (m):</label>
				<div class="col-8">
					<input class="form-control" type="text" id="eye_height" name="eye_height" value="%(eye_height)s" required pattern="^\d+(\.\d+)?\s*$"><br>
				</div>
			</div>

			<div class="form-group row">
				<label for="fetch" class="col-4 col-form-label">Dip Short Fetch (m):</label>
				<div class="col-8">
					<input class="form-control" type="text" id="fetch" name="fetch" value="%(fetch)s" pattern="^(\d{3,}(\.\d+)?)?$"><br>
				</div>
			</div>

			<div class="text-center">
				<button type="submit" class="btn btn-primary" name="submit" value="submit">Get Hs</button>
			</div>
			</div>
		</form>
		<div class="mb-4 p-5 text-center">
			<h1 class="display-1 fw-bold">%(hs)s</h1>
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
