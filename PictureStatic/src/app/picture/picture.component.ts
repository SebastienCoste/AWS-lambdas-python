import { Picture } from './picture.service';
import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-picture',
  templateUrl: './picture.component.html',
  styleUrls: ['./picture.component.css']
})
export class PictureComponent  {

  constructor() { }

    @Input() picture: Picture;
}
