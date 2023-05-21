<!DOCTYPE html>
<html>
<body>
    <textarea id="userInput"></textarea>
    <h1 id="welcomeMessage">Welcome ${msg}</h1>

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script>
        $(document).ready(function() {
            $('#userInput').on('input', function() {
                var userInput = $(this).val();
                $.post("/process", { userInput: userInput }, function(data) {
                    $('#welcomeMessage').text("Welcome " + data);
                });
            });
        });
    </script>
</body>
</html>


