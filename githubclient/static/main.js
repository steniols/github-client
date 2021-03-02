var toastElList = [].slice.call(document.querySelectorAll('.toast'))
var toastList = toastElList.map(function (toastEl) {
  toast = new bootstrap.Toast(toastEl)
  toast.show()
})

if (document.getElementById('tagRelationshipModal') != null) {
  var tagRelationshipModal = document.getElementById('tagRelationshipModal')
  tagRelationshipModal.addEventListener('show.bs.modal', function (event) {
    var button = event.relatedTarget
    var recipient = button.getAttribute('data-bs-id')
    var githubProjectInput = tagRelationshipModal.querySelector('#tagRelationshipModal input[name="github_project_id"]')
    githubProjectInput.value = recipient
    var tagsSelect = tagRelationshipModal.querySelector('#tagRelationshipModal select[name="tags"]')
    
    var ajax = new XMLHttpRequest();
    ajax.open("GET", "tags/getTags", true);
    ajax.send();
    ajax.onreadystatechange = function() {      
      if (ajax.readyState == 4 && ajax.status == 200) {
        var data = ajax.responseText;
        var tags = JSON.parse(data)
        tagsSelect.innerHTML = '';
        for (let [key, value] of Object.entries(tags)) {
          var opt = document.createElement('option');
          opt.value = key;
          opt.innerHTML = value;
          tagsSelect.appendChild(opt);
        }
      }
    }
  })
}

if (document.getElementById('relationshipRemoveModal') != null) {
  var relationshipRemoveModal = document.getElementById('relationshipRemoveModal')
  relationshipRemoveModal.addEventListener('show.bs.modal', function (event) {
    var button = event.relatedTarget
    var tagId = button.getAttribute('data-tag-id')
    var tagInput = relationshipRemoveModal.querySelector('#relationshipRemoveModal input[name="tag_id"]')
    tagInput.value = tagId
    var repositoryId = button.getAttribute('data-repository-id')
    var repositoryInput = relationshipRemoveModal.querySelector('#relationshipRemoveModal input[name="repository_id"]')
    repositoryInput.value = repositoryId
  })
}

if (document.getElementById('deleteTagModal') != null) {
  var deleteTagModal = document.getElementById('deleteTagModal')
  deleteTagModal.addEventListener('show.bs.modal', function (event) {
    var button = event.relatedTarget
    var recipient = button.getAttribute('data-bs-id')
    var modalBodyInput = deleteTagModal.querySelector('#deleteTagModal input[name="tag_id"]')
    modalBodyInput.value = recipient
  })
}
