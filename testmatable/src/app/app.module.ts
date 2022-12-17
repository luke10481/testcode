import { NgModule } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";
import { FormsModule } from "@angular/forms";

import { AppComponent } from "./app.component";
import { HelloComponent } from "./hello.component";
import { ModalComponent } from "./modal/modal.component";

import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
import { MatTableModule } from "@angular/material";
import { MatButtonModule } from "@angular/material";
import { MatIconModule } from "@angular/material";
import { MatDialogModule, MatFormFieldModule, MatInputModule } from "@angular/material";

@NgModule({
  imports: [
    BrowserModule,
    FormsModule,
    BrowserAnimationsModule,
    MatTableModule,
    MatIconModule,
    MatButtonModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule
  ],
  declarations: [AppComponent, HelloComponent, ModalComponent],
  bootstrap: [AppComponent],
  entryComponents: [ModalComponent]
})
export class AppModule {}
