import { Injectable } from '@angular/core';
import * as data from '../lambdaReport.json';
import { Http, Response } from '@angular/http';
import 'rxjs/add/operator/map';

export class Picture {
  constructor(public name: string, public link: string) { }
}

@Injectable()
export class PictureService {

  
  url: '';

  constructor( private http: Http ) { }

  getPictures(){
      console.log('avant' + this.url);

    if (this.url === '' || this.url === undefined){
      this.url = (<any>data).allLambdas.find(myObj => myObj.name === 'photos').url;
      console.log('loaded URL: ' + this.url);
    }
//'https://g280jcy3mh.execute-api.eu-west-1.amazonaws.com/v1/retrieve'
    return this.http.post(this.url, null)
      .map((res: Response) => res.json());
  }

  getUrl(){

    console.log('loading lambda urls')
    return this.http.get('c.json').map((res: Response) => res.json());
  }
}
