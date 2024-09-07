<link rel="stylesheet" href="https://formflow.org/styles.css" />
<form
    class="formflow"
    id="formflow"
    action="https://api.formflow.org"
    method="POST"
    enctype="multipart/form-data"
>
    <!-- REQUIRED FIELDS: user_id -->
    <input type="hidden" name="user_id" value="user_id_mhOmxMBPWlxrOpYOlzJLvg" />
    <label for="field-message">Message:</label>
    <textarea id="field-message" name="Message" placeholder="Message"></textarea>
    <label for="field-attachments">File attachments:</label>
    <input type="file" name="Attachments" multiple />
    <button type="submit">Send</button>
</form>
<script src="https://hikaru.org/js/FRM.js"></script>
<script>FRM.listen(document.getElementById("formflow"));</script>
