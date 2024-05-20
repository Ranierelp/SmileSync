const inputFile = document.querySelector("#picture_input");
const pictureImage = document.querySelector(".picture_image");
const pictureImageSrc = pictureImage.getAttribute("data-default-src");
const pictureImageTxt = `<img src="${pictureImageSrc}" alt="Profile Icon" class="img-fluid">`;
pictureImage.innerHTML = pictureImageTxt;

inputFile.addEventListener("change", function (e) {
  const inputTarget = e.target;
  const file = inputTarget.files[0];

  if (file) {
    const reader = new FileReader();

    reader.addEventListener("load", function (e) {
      const readerTarget = e.target;

      const img = document.createElement("img");
      img.src = readerTarget.result;
      img.classList.add("picture_img");

      pictureImage.innerHTML = "";
      pictureImage.appendChild(img);
    });

    reader.readAsDataURL(file);
  } else {
    pictureImage.innerHTML = pictureImageTxt;
  }
});
