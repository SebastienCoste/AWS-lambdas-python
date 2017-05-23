import { PictureComponent } from '../picture/picture.component';
import { Component, OnInit } from '@angular/core';
import { Picture, PictureService } from '../picture/picture.service'
@Component({
  selector: 'app-pictures',
  templateUrl: './pictures.component.html',
  styleUrls: ['./pictures.component.css'],
  providers: [PictureService]
})
export class PicturesComponent implements OnInit {

  pictures: Picture[];
  selectedPicture: Picture;

  constructor(private pictureService: PictureService) { }

  ngOnInit() {
    this.pictureService.getPictures()
      .subscribe(pictures => this.pictures = pictures.pics);
    }

  onSelect(picture: Picture){
    this.selectedPicture = picture;

  }
}



