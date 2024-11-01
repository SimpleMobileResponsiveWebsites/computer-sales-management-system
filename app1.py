import datetime
from dataclasses import dataclass
from typing import List, Dict
from enum import Enum

class SaleType(Enum):
    WHOLESALE = "wholesale"
    RETAIL = "retail"

@dataclass
class Computer:
    id: str
    brand: str
    model: str
    specs: Dict[str, str]
    wholesale_price: float
    retail_price: float
    stock: int

class ComputerInventory:
    def __init__(self):
        self.computers: Dict[str, Computer] = {}
        self.sales_history: List[Dict] = []

    def add_computer(self, computer: Computer) -> None:
        """Add a new computer to inventory."""
        self.computers[computer.id] = computer

    def remove_computer(self, computer_id: str) -> None:
        """Remove a computer from inventory."""
        if computer_id in self.computers:
            del self.computers[computer_id]

    def update_stock(self, computer_id: str, quantity: int) -> bool:
        """Update stock quantity for a computer."""
        if computer_id in self.computers:
            self.computers[computer_id].stock += quantity
            return True
        return False

    def process_sale(self, computer_id: str, quantity: int, sale_type: SaleType) -> Dict:
        """Process a sale transaction."""
        if computer_id not in self.computers:
            raise ValueError("Computer not found")

        computer = self.computers[computer_id]
        if computer.stock < quantity:
            raise ValueError("Insufficient stock")

        price = (
            computer.wholesale_price if sale_type == SaleType.WHOLESALE 
            else computer.retail_price
        )
        total_price = price * quantity

        # Update stock
        computer.stock -= quantity

        # Record sale
        sale_record = {
            "date": datetime.datetime.now(),
            "computer_id": computer_id,
            "quantity": quantity,
            "sale_type": sale_type.value,
            "total_price": total_price,
            "unit_price": price
        }
        self.sales_history.append(sale_record)
        return sale_record

    def get_inventory_report(self) -> Dict:
        """Generate inventory report."""
        return {
            "total_computers": len(self.computers),
            "total_stock": sum(c.stock for c in self.computers.values()),
            "total_wholesale_value": sum(
                c.stock * c.wholesale_price for c in self.computers.values()
            ),
            "total_retail_value": sum(
                c.stock * c.retail_price for c in self.computers.values()
            )
        }

    def get_sales_report(self, start_date: datetime.datetime = None) -> Dict:
        """Generate sales report."""
        if start_date is None:
            start_date = datetime.datetime.min

        filtered_sales = [
            sale for sale in self.sales_history 
            if sale["date"] >= start_date
        ]

        wholesale_sales = sum(
            sale["total_price"] 
            for sale in filtered_sales 
            if sale["sale_type"] == SaleType.WHOLESALE.value
        )
        retail_sales = sum(
            sale["total_price"] 
            for sale in filtered_sales 
            if sale["sale_type"] == SaleType.RETAIL.value
        )

        return {
            "total_sales": len(filtered_sales),
            "wholesale_revenue": wholesale_sales,
            "retail_revenue": retail_sales,
            "total_revenue": wholesale_sales + retail_sales
        }

# Example usage
def main():
    # Initialize inventory system
    inventory = ComputerInventory()

    # Add sample computers
    sample_computer = Computer(
        id="LP001",
        brand="LaptopBrand",
        model="Pro2024",
        specs={
            "processor": "Intel i7",
            "ram": "16GB",
            "storage": "512GB SSD"
        },
        wholesale_price=800.00,
        retail_price=1200.00,
        stock=10
    )
    inventory.add_computer(sample_computer)

    # Process sample sales
    try:
        # Process a wholesale sale
        wholesale_sale = inventory.process_sale(
            "LP001", 
            quantity=3, 
            sale_type=SaleType.WHOLESALE
        )
        print(f"Wholesale sale processed: {wholesale_sale}")

        # Process a retail sale
        retail_sale = inventory.process_sale(
            "LP001", 
            quantity=1, 
            sale_type=SaleType.RETAIL
        )
        print(f"Retail sale processed: {retail_sale}")

        # Generate reports
        inventory_report = inventory.get_inventory_report()
        sales_report = inventory.get_sales_report()

        print("\nInventory Report:")
        print(inventory_report)
        print("\nSales Report:")
        print(sales_report)

    except ValueError as e:
        print(f"Error processing sale: {e}")

if __name__ == "__main__":
    main()
