import { Component } from "@angular/core";
import { MatTableDataSource } from "@angular/material";
import { MatDialog, MatDialogConfig } from "@angular/material";
import { ModalComponent } from "./modal/modal.component";
import { FormControl } from "@angular/forms";

@Component({
  selector: "my-app",
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.css"]
})
export class AppComponent {
  constructor(private dialog: MatDialog) {}
  name = "Angular 5";
  displayedColumns = ["position", "name", "weight", "symbol", "actions"];
  dataSource = new MatTableDataSource<Element>(ELEMENT_DATA);
  highlightedRows = [];
  highlightedRowss = {};
  isDisabled = false;

  onChange() {
    const dialogConfig = new MatDialogConfig();
    // dialogConfig.disableClose = true;
    dialogConfig.autoFocus = true;
    dialogConfig.width = "60%";
    this.dialog.open(ModalComponent, dialogConfig);
  }

  highlight(row) {
    this.highlightedRows.push(row);
    this.highlightedRowss[row.name] = !this.highlightedRowss[row.name];
  }

  applyFilter(filter: string) {
    this.dataSource.filter = filter;
  }
}

export interface Element {
  name: string;
  position: number;
  weight: number;
  symbol: string;
}

const ELEMENT_DATA: Element[] = [
  { position: 1, name: "Hydrogen Lithium", weight: 1.0079, symbol: "H" },
  { position: 2, name: "Helium Beryllium", weight: 4.0026, symbol: "He" },
  { position: 3, name: "Lithium Carbon", weight: 6.941, symbol: "Li" },
  { position: 4, name: "Beryllium Carbon", weight: 9.0122, symbol: "Be" },
  { position: 5, name: "Boron Nitrogen", weight: 10.811, symbol: "B" },
  { position: 6, name: "Carbon Oxygen", weight: 12.0107, symbol: "C" },
  { position: 7, name: "Nitrogen Fluorine", weight: 14.0067, symbol: "N" },
  { position: 8, name: "Oxygen Neon", weight: 15.9994, symbol: "O" },
  { position: 9, name: "Fluorine Sodium", weight: 18.9984, symbol: "F" },
  { position: 10, name: "Neon Sodium", weight: 20.1797, symbol: "Ne" },
  { position: 11, name: "Sodium Magnesium", weight: 22.9897, symbol: "Na" },
  { position: 12, name: "Magnesium Aluminum", weight: 24.305, symbol: "Mg" },
  { position: 13, name: "Aluminum Silicon", weight: 26.9815, symbol: "Al" },
  { position: 14, name: "Silicon Phosphorus", weight: 28.0855, symbol: "Si" },
  { position: 15, name: "Phosphorus Sulfur", weight: 30.9738, symbol: "P" },
  { position: 16, name: "Sulfur Chlorine", weight: 32.065, symbol: "S" },
  { position: 17, name: "Chlorine Argon", weight: 35.453, symbol: "Cl" },
  { position: 18, name: "Argon Potassium", weight: 39.948, symbol: "Ar" },
  { position: 19, name: "Potassium Calcium", weight: 39.0983, symbol: "K" },
  { position: 20, name: "Calcium Potassium", weight: 40.078, symbol: "Ca" }
];
