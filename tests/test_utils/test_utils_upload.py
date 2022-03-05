from project.utils.upload import image_upload, image_remove_and_upload, image_remove

def test_image_upload_and_image_remove(example_image):
    uploaded = image_upload(example_image)
    assert uploaded != None, "Não salvou a imagem"
    removed = image_remove(uploaded)
    assert removed == uploaded, "A imagem removida não tem o mesmo nome que a imagem inserida"
    
def test_image_upload_is_none(example_image):
    uploaded = image_upload(None)
    assert uploaded == None, "Deve retornar None em imagem vazia"

def test_image_remove_is_none(example_image):
    uploaded = image_remove(None)
    assert uploaded == None, "Deve retornar None em imagem vazia"
    
def test_image_remove_and_upload(example_image):
    uploaded = image_remove_and_upload(example_image, example_image.filename)
    assert uploaded != None, "Não salvou a imagem"
    removed = image_remove(uploaded)
    assert removed == uploaded, "A imagem removida não tem o mesmo nome que a imagem inserida"

def test_image_remove_and_upload_new_file_is_none(example_image):
    uploaded = image_upload(example_image)
    re_uploaded = image_remove_and_upload(None, uploaded)
    assert re_uploaded == None, "Inseriu uma imagem inexistente, e não removeu."
    
def test_image_remove_and_upload_new_file_but_already_exists_image(example_image):
    uploaded = image_upload(example_image)
    re_uploaded = image_remove_and_upload(example_image, uploaded)
    assert re_uploaded != None, "Não salvou a imagem"
    