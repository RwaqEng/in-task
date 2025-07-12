<script>
document.querySelectorAll('#editMode input, #editMode select').forEach(field => {
    field.addEventListener('change', () => {
        const form = document.getElementById('profileForm');
        const formData = new FormData(form);

        fetch('/api/profile', {
            method: 'PUT',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                toastr.success('تم حفظ التعديل تلقائيًا');
            } else {
                toastr.error('خطأ: ' + data.message);
            }
        })
        .catch(() => {
            toastr.error('حدث خطأ في الاتصال');
        });
    });
});
</script>