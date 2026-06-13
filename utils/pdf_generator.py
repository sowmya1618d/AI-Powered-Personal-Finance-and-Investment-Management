"""
Monthly PDF Report Generator
Creates comprehensive financial reports
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from datetime import datetime, date
from typing import Dict, List
import os


class MonthlyReportGenerator:
    """Generate monthly financial PDF reports"""
    
    def __init__(self, output_dir: str = "reports/"):
        """
        Initialize report generator
        
        Args:
            output_dir: Directory to save reports
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        self.styles = getSampleStyleSheet()
        
        # Custom styles
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6
        )
    
    def generate_report(
        self,
        user_name: str,
        month: date,
        income_data: Dict,
        expense_data: Dict,
        assets_data: Dict,
        liabilities_data: Dict,
        net_worth_data: Dict,
        predictions: Dict = None
    ) -> str:
        """
        Generate comprehensive monthly report
        
        Args:
            user_name: User's name
            month: Report month
            income_data: Income information
            expense_data: Expense information
            assets_data: Assets information
            liabilities_data: Liabilities information
            net_worth_data: Net worth information
            predictions: ML predictions
        
        Returns:
            Path to generated PDF
        """
        # Create filename
        month_str = month.strftime("%Y-%m")
        filename = f"{self.output_dir}financial_report_{month_str}.pdf"
        
        # Create PDF document
        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Container for PDF elements
        story = []
        
        # Title
        title = Paragraph(
            f"Monthly Financial Report<br/>{month.strftime('%B %Y')}",
            self.title_style
        )
        story.append(title)
        story.append(Spacer(1, 0.2*inch))
        
        # User Info
        user_info = Paragraph(
            f"<b>Name:</b> {user_name}<br/>"
            f"<b>Report Generated:</b> {datetime.now().strftime('%d %B %Y, %I:%M %p')}",
            self.normal_style
        )
        story.append(user_info)
        story.append(Spacer(1, 0.3*inch))
        
        # === INCOME SECTION ===
        story.append(Paragraph("💰 Income Summary", self.heading_style))
        
        income_table_data = [
            ["Source", "Amount (₹)"],
            ["Salary", f"₹{income_data.get('salary', 0):,.2f}"],
            ["Other Income", f"₹{income_data.get('other_income', 0):,.2f}"],
            ["Total Income", f"₹{income_data.get('total', 0):,.2f}"]
        ]
        
        income_table = Table(income_table_data, colWidths=[3*inch, 2*inch])
        income_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#ecf0f1')),
        ]))
        story.append(income_table)
        story.append(Spacer(1, 0.3*inch))
        
        # === EXPENSE SECTION ===
        story.append(Paragraph("💸 Expense Summary", self.heading_style))
        
        expense_table_data = [["Category", "Amount (₹)", "% of Total"]]
        total_expenses = expense_data.get('total', 0)
        
        for category, amount in expense_data.get('categories', {}).items():
            percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
            expense_table_data.append([
                category,
                f"₹{amount:,.2f}",
                f"{percentage:.1f}%"
            ])
        
        expense_table_data.append([
            "Total Expenses",
            f"₹{total_expenses:,.2f}",
            "100%"
        ])
        
        expense_table = Table(expense_table_data, colWidths=[2.5*inch, 1.5*inch, 1*inch])
        expense_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (2, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#ecf0f1')),
        ]))
        story.append(expense_table)
        story.append(Spacer(1, 0.3*inch))
        
        # === SAVINGS SECTION ===
        savings = income_data.get('total', 0) - total_expenses
        savings_rate = (savings / income_data.get('total', 1) * 100) if income_data.get('total', 0) > 0 else 0
        
        story.append(Paragraph("💵 Savings", self.heading_style))
        savings_info = Paragraph(
            f"<b>Monthly Savings:</b> ₹{savings:,.2f}<br/>"
            f"<b>Savings Rate:</b> {savings_rate:.1f}%",
            self.normal_style
        )
        story.append(savings_info)
        story.append(Spacer(1, 0.3*inch))
        
        # === ASSETS SECTION ===
        story.append(Paragraph("📈 Assets", self.heading_style))
        
        assets_table_data = [
            ["Asset Type", "Value (₹)"],
            ["Stocks", f"₹{assets_data.get('stocks', 0):,.2f}"],
            ["SIP", f"₹{assets_data.get('sip', 0):,.2f}"],
            ["Mutual Funds", f"₹{assets_data.get('mutual_funds', 0):,.2f}"],
            ["Fixed Deposits", f"₹{assets_data.get('fd', 0):,.2f}"],
            ["Savings", f"₹{assets_data.get('savings', 0):,.2f}"],
            ["Total Assets", f"₹{assets_data.get('total', 0):,.2f}"]
        ]
        
        assets_table = Table(assets_table_data, colWidths=[3*inch, 2*inch])
        assets_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#d5f4e6')),
        ]))
        story.append(assets_table)
        story.append(Spacer(1, 0.3*inch))
        
        # === LIABILITIES SECTION ===
        story.append(Paragraph("📉 Liabilities", self.heading_style))
        
        liabilities_table_data = [
            ["Liability Type", "Amount (₹)"],
            ["Home Loan", f"₹{liabilities_data.get('home_loan', 0):,.2f}"],
            ["Personal Loan", f"₹{liabilities_data.get('personal_loan', 0):,.2f}"],
            ["Credit Card", f"₹{liabilities_data.get('credit_card', 0):,.2f}"],
            ["Total Liabilities", f"₹{liabilities_data.get('total', 0):,.2f}"]
        ]
        
        liabilities_table = Table(liabilities_table_data, colWidths=[3*inch, 2*inch])
        liabilities_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e67e22')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#fdebd0')),
        ]))
        story.append(liabilities_table)
        story.append(Spacer(1, 0.3*inch))
        
        # === NET WORTH SECTION ===
        story.append(Paragraph("💎 Net Worth", self.heading_style))
        
        net_worth = net_worth_data.get('net_worth', 0)
        prev_net_worth = net_worth_data.get('previous_month', 0)
        change = net_worth - prev_net_worth
        change_pct = (change / prev_net_worth * 100) if prev_net_worth > 0 else 0
        
        net_worth_info = Paragraph(
            f"<b>Current Net Worth:</b> ₹{net_worth:,.2f}<br/>"
            f"<b>Previous Month:</b> ₹{prev_net_worth:,.2f}<br/>"
            f"<b>Change:</b> ₹{change:,.2f} ({change_pct:+.2f}%)",
            self.normal_style
        )
        story.append(net_worth_info)
        story.append(Spacer(1, 0.3*inch))
        
        # === PREDICTIONS SECTION ===
        if predictions:
            story.append(Paragraph("🔮 AI Predictions", self.heading_style))
            
            predictions_info = Paragraph(
                f"<b>Predicted Net Worth (Next Month):</b> ₹{predictions.get('next_month', 0):,.2f}<br/>"
                f"<b>Predicted Return:</b> {predictions.get('expected_return', 0):.2f}%<br/>"
                f"<b>Risk Score:</b> {predictions.get('risk_score', 'Medium')}",
                self.normal_style
            )
            story.append(predictions_info)
            story.append(Spacer(1, 0.3*inch))
        
        # === FOOTER ===
        story.append(Spacer(1, 0.5*inch))
        footer = Paragraph(
            "<i>This report is generated automatically by AI Personal Finance Manager. "
            "Please verify all data and consult a financial advisor for investment decisions.</i>",
            self.normal_style
        )
        story.append(footer)
        
        # Build PDF
        doc.build(story)
        
        print(f"✅ PDF report generated: {filename}")
        return filename


# Global instance
report_generator = MonthlyReportGenerator()
