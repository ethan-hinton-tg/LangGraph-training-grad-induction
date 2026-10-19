"""Deterministic fictional CPG data. Pass Spark explicitly; imports never write."""

from datetime import date, timedelta
import re


REGIONS = ("Midwest", "Northeast", "Southeast", "Southwest", "West")
RETAILERS = ("NorthMart", "FreshCo", "ValueWay", "MarketSquare")
PRODUCT_LINES = (
    ("OAT", "Plant-based drinks", "Oat Drink", "1 litre", 3.49,
     ("Original", "Barista", "Unsweetened", "Vanilla")),
    ("GRN", "Breakfast", "Granola", "400 grams", 4.79,
     ("Honey Almond", "Berry", "Low Sugar", "Chocolate")),
    ("SOUP", "Pantry meals", "Soup", "500 grams", 3.29,
     ("Tomato", "Lentil", "Roasted Vegetable", "Minestrone")),
    ("SNK", "Snacks", "Baked Crisps", "120 grams", 2.59,
     ("Sea Salt", "Paprika", "Sour Cream", "Herb")),
    ("YOG", "Chilled dairy", "Yogurt", "450 grams", 2.99,
     ("Natural", "Strawberry", "Peach", "Greek Style")),
    ("SAUCE", "Cooking sauces", "Cooking Sauce", "350 grams", 3.89,
     ("Basil Tomato", "Arrabbiata", "Coconut Curry", "Roasted Pepper")),
)


def _products():
    products = []
    for prefix, category, line, size, price, variants in PRODUCT_LINES:
        for number, variant in enumerate(variants, 1):
            name = "Northstar Oat Drink" if (prefix, number) == ("OAT", 1) else f"Northstar {variant} {line}"
            products.append({
                "product_id": f"{prefix}-{number}", "product_name": name,
                "category": category, "variant": variant, "pack_size": size,
                "list_price": round(price + (number - 1) * 0.2, 2),
                "storage": "Chilled" if prefix == "YOG" else "Ambient",
                "shelf_life_days": 28 if prefix == "YOG" else 270,
            })
    return products


def _document(document_id, title, paragraphs, product_id="", region="", retailer=""):
    return (document_id, title, "\n\n".join(paragraphs), product_id, region, retailer)


def _documents(products):
    methodology = [
        "Scope and evidence standard. Northstar Foods is a fictional consumer-goods business. Its commercial teams sell plant-based drinks, breakfast cereals, pantry meals, snacks, chilled dairy and cooking sauces through grocery accounts. This training corpus combines synthetic operational records with fictional internal documents. Narrative records describe plans, reports and working hypotheses. They are not verified experimental evidence. An analyst must separate measured sales from account-team commentary and identify the reporting period, geography, retailer and product before comparing results.",
        "Measurement conventions. Weekly sales are units assigned to the Sunday week-start label; they are not individual checkout events. Monthly summaries use the month of that label rather than allocating a week across calendar boundaries. Availability is a weekly proportion, averaged without weighting unless explicitly stated. Different stores can contribute to different weekly observations. The dataset does not contain store-level exposure, customer switching, competitor prices or weather measurements. These omissions limit what can be inferred about consumer demand or lost sales.",
        "Promotion interpretation. The promotions table records planned account offers and their inclusive start and end dates. Date overlap indicates a recorded offer relevant to a reporting window, not evidence that every store activated it or every shopper saw it. A missing matching row means no promotion is recorded in this training dataset. It does not establish that an account ran no other activity. Changes in promotion, distribution, shelf position and supply can happen together, so attributing an observed movement to one factor requires additional evidence.",
        "Operational context. Shipment quantities represent synthetic dispatch activity, not confirmed shelf replenishment or customer purchases. A delayed shipment can coexist with adequate store stock, while an on-time shipment may still be unavailable to shoppers. Account plans should be checked against completion logs, receiving scans and store observations before being described as executed events. Cross-category comparisons also require attention to pack size, price, storage requirements and product lifecycle. Units are appropriate within a product, but are not a universal measure of category value.",
        "Analysis workflow. First retrieve the relevant structured records and check whether the comparison includes the same product, retailer and region in both periods. Then gather documents with dates and account scope matching the question. Keep document identifiers and titles beside the retrieved text so another analyst can verify each statement. If a passage is unrelated, outdated or too broad, state that limitation instead of treating keyword overlap as support. Separate observations, documentary context and unresolved questions in the final summary.",
        "Governance and next actions. Commercial analysts should avoid publishing sensitive account information outside approved channels, even when using synthetic data during training. A production investigation would request store-level availability, confirmed promotional execution, comparable distribution and a longer baseline. The team would compare exposed and unexposed stores where feasible and document alternative explanations. Until those checks are complete, the appropriate language is consistent with, coincided with or may be relevant, rather than caused or proved. This policy applies to every Northstar product and account.",
    ]
    documents = [
        _document("DOC-ACCOUNT-PLAN-MAY25", "NorthMart Midwest account plan, May 2025", [
            "A shelf reset is scheduled to begin on May 12 in approximately 20% of NorthMart Midwest locations. The account team should monitor product availability during the transition. This document records a plan and does not confirm which stores completed the reset. The scope is the Midwest NorthMart oat-drink fixture, not every retailer or product. The commercial team has not supplied a store-level completion log or measured sales effect. Planned dates must not be presented as confirmed execution dates.",
            "Account objectives. The team intends to review the plant-based beverage bay and clarify shelf labels for original and barista products. Existing facings should remain visible while stores change layouts. Store managers are asked to report damaged labels, blocked replenishment access and missing shelf tickets through normal account channels. These are proposed operating instructions rather than a record of compliance. This plan contains no control group, no exposure counts by product and no evidence that the intended layout improved or reduced shopper conversion.",
            "Monitoring requests. The account analyst should compare April and May OAT-1 weekly units and in-stock observations separately for NorthMart and FreshCo in the Midwest. FreshCo is a useful descriptive comparison, but differences in store mix prevent treating it as a causal control. The account team wants to see whether availability changes occur before, during or after the proposed reset window. A weekly aggregate alone cannot establish the timing at individual stores, and a broader monthly decline does not identify its mechanism.",
            "Follow-up ownership. NorthMart field representatives would collect completion dates and store photographs, while the Northstar supply team would reconcile receiving exceptions. Neither evidence set is included in this workshop. If the agent references this account plan, it should cite DOC-ACCOUNT-PLAN-MAY25 and explicitly retain the scheduled, approximately and not confirmed qualifications. Other regions have their own account calendars. The absence of a matching Northeast oat-drink sales record in this dataset must not be filled with Midwest observations.",
        ] + methodology[2:4], "OAT-1", "Midwest", "NorthMart"),
        _document("DOC-PROMO-BRIEF-APR25", "NorthMart oat drink promotion brief, April 2025", [
            "The NorthMart Midwest spring oat-drink promotion is planned to run from April 1 through April 21 with a 10% discount. No May promotion is listed in this brief. The relevant product is OAT-1, Northstar Oat Drink. The plan describes a temporary price offer at one retailer and region. It is not an audit of till prices, shopper exposure or completed display activity. The brief does not assert that ending the offer explains the subsequent change in units sold.",
            "Commercial rationale. The offer is intended to support spring household trial of the original one-litre oat drink. Account teams may provide recipe cards for porridge and smoothies where retailer approval allows, but this document does not record which stores used those materials. Promotional effectiveness should consider base sales, comparable availability and repeat purchase after the offer. A simple before-and-after comparison is vulnerable to coincident distribution or supply changes and cannot isolate incremental promotional sales without further assumptions.",
            "Scope boundaries. FreshCo has a separate Midwest featured-item record from April 7 through April 13 at a 5% discount. That offer should not be merged into NorthMart's activity or applied across all of April. Other Northstar categories and regions use different calendars. An overlap query can find recorded offers within a requested window, while a monthly sales aggregate includes complete weekly labels. Analysts should disclose those differing time conventions rather than imply an exact transaction-level join between the tables.",
            "Reporting request. Prepare April and May retailer totals and list the recorded offer dates beside them. If no May row matches, use the wording no May promotion is recorded in the supplied dataset or this brief, not no promotion occurred. The account manager would need retailer execution records to confirm actual offers. Cite this brief by title or DOC-PROMO-BRIEF-APR25 when discussing its contents. Avoid claims about price elasticity, customer loyalty or profitability that the available fields cannot support.",
        ] + methodology[1:3], "OAT-1", "Midwest", "NorthMart"),
        _document("DOC-SUPPLY-NOTE-MAY25", "Midwest replenishment note, May 2025", [
            "The operations team reported replenishment delays affecting some NorthMart Midwest shipments during May. This note does not quantify the impact on store-level availability or sales. The team has not provided affected store identifiers, delay durations or confirmed lost units. Its scope is NorthMart Midwest and the oat-drink account discussion. The existence of reported delays is documentary context, not proof that the delays caused the April-to-May OAT-1 decline or that every store experienced the same problem.",
            "Investigation questions. Operations would reconcile dispatch dates against retailer receiving scans and review whether delayed deliveries arrived before existing shelf stock ran out. Warehouse fill rate, retailer backroom stock and shelf replenishment are distinct stages. A dispatch record cannot substitute for a shelf observation. The team also wants to determine whether order changes, delivery appointment constraints or handling exceptions contributed to the reported delays. These remain questions in this note and must not be rewritten as established findings.",
            "Product handling. Ambient oat drinks have different storage and shelf-life requirements from chilled yogurt. The account team should not generalize a beverage replenishment note to dairy shipments, granola or cooking sauces. Synthetic shipment rows in the workshop provide extra operational context, but are not underlying evidence validating this qualitative report. Their simulated values cannot estimate a real-world effect. Analysts comparing datasets should state that they are practicing query and retrieval workflows with deliberately designed fictional records.",
            "Requested evidence. Store-level out-of-stock intervals, opening inventory, replenishment scans, order fill and comparable sales would help quantify potential impact. A confirmed sequence of events would still require consideration of promotions, distribution and shopper demand. The agent should cite DOC-SUPPLY-NOTE-MAY25, describe the delays as reported, and state that their effect is unquantified. If asked to identify a demonstrated cause, the appropriate answer is that these tables and documents do not establish one.",
        ] + methodology[3:5], "OAT-1", "Midwest", "NorthMart"),
        _document("DOC-COMPANY-OVERVIEW-2025", "Northstar Foods company overview and evidence policy, 2025", methodology),
        _document("DOC-METRICS-HANDBOOK-2025", "Northstar commercial metrics handbook, 2025", methodology[1:] + methodology[:1]),
    ]
    category_notes = {
        "Plant-based drinks": ("breakfast, smoothies and coffee", "ambient beverage aisles", "cafe trial and household repeat purchase"),
        "Breakfast": ("weekday breakfasts and lunchbox toppings", "cereal and breakfast aisles", "pack visibility and flavour range"),
        "Pantry meals": ("quick lunches and evening meals", "ambient meal aisles", "meal occasions and seasonal demand"),
        "Snacks": ("shared lunches and on-the-go occasions", "savoury snack aisles", "display space and impulse purchases"),
        "Chilled dairy": ("breakfast and chilled snacking", "refrigerated dairy bays", "cold-chain handling and stock rotation"),
        "Cooking sauces": ("weeknight home cooking", "cooking ingredients aisles", "recipe inspiration and pantry replenishment"),
    }
    for product in products:
        product_id = product["product_id"]
        name = product["product_name"]
        occasions, placement, priorities = category_notes[product["category"]]
        documents.append(_document(f"DOC-PRODUCT-{product_id}-2025", f"{name}: product and commercial playbook, 2025", [
            f"Portfolio role. {name} ({product_id}) belongs to Northstar's {product['category']} range. The variant is {product['variant']} and the consumer pack is {product['pack_size']}. The indicative list price is ${product['list_price']:.2f}; actual recorded prices may differ by account, week and promotion. The product is designed for {occasions}. This playbook explains positioning and operating expectations, not measured market share or customer preferences. Product names and identifiers should be retained together when summarizing records so similar variants are not combined accidentally.",
            f"Merchandising guidance. Retailers normally position {name} in {placement}. Commercial reviews should focus on {priorities}, while respecting account-specific layouts. Teams may suggest clear shelf labels, consistent product grouping and appropriate stock depth. These suggestions are not evidence that a retailer implemented them. A placement change should be confirmed with dated store observations before being used to explain sales. The same category can behave differently in NorthMart, FreshCo, ValueWay and MarketSquare because assortment and shopper missions differ.",
            f"Handling and replenishment. {product_id} uses {product['storage'].lower()} storage and an indicative shelf life of {product['shelf_life_days']} days. Replenishment teams should review expiry rotation, case handling and inventory accuracy rather than infer shelf availability from dispatched units alone. In the synthetic tables, shipment fill rate is requested versus shipped units, while in-stock rate represents a separate weekly observation. Neither measure contains store-level exposure. For {name}, a decline in one measure can motivate investigation but does not establish the direction or size of a sales effect.",
            f"Promotion planning. Offers for {name} should be read from the promotions table using product, region, retailer and overlapping dates. Generic category guidance must not be treated as an offer record. Analysts should distinguish the list price in the product master from simulated weekly selling price, and avoid assuming a planned discount was executed at every store. This playbook does not supply incremental volume, margin or shopper-panel measures. A seasonal peak or temporary offer can coincide with other commercial changes, so comparisons should retain those limitations.",
            f"Range and geography. The broader Northstar dataset covers Midwest, Northeast, Southeast, Southwest and West for most products. OAT-1 deliberately has no Northeast observations, and its Midwest case uses only NorthMart and FreshCo. Those are training coverage boundaries, not claims about real distribution. For {product_id}, check the actual filtered rows before claiming a regional result. Comparing variants should use explicit identifiers: {name} must not be silently substituted for another flavour, pack or category when a user asks an ambiguous question.",
            f"Recommended analysis. Start with units for {product_id} in the requested dates and region, then inspect retailer contributions, availability and recorded offers. If the question mentions operational changes, retrieve an appropriately scoped account or supply document. Cite this playbook as DOC-PRODUCT-{product_id}-2025 only for product context that it actually contains. Separate measured observations from planned actions and explain missing evidence. Before recommending a commercial intervention, request execution logs or an evaluation design capable of distinguishing competing explanations rather than interpreting a descriptive association as a causal result.",
        ], product_id=product_id))
    for region_number, region in enumerate(REGIONS):
        for retailer_number, retailer in enumerate(RETAILERS):
            focus = products[(region_number * 4 + retailer_number * 3) % len(products)]
            initiative = ("assortment review", "shelf-label audit", "seasonal display trial", "replenishment review")[retailer_number]
            documents.append(_document(f"DOC-ACCOUNT-{region.upper()}-{retailer.upper()}-2025", f"{retailer} {region}: annual account operating plan, 2025", [
                f"Account scope. This plan covers the {retailer} account in the {region} region for the 2025 planning cycle. A proposed {initiative} is the principal working initiative, with {focus['product_name']} ({focus['product_id']}) as one discussion example. The proposal is not a completion report and does not assert an observed sales effect. The account stocks a mix of Northstar categories, and analysts must query actual product-region-retailer records rather than assume every portfolio item has matching observations.",
                f"Planning calendar. The {retailer} {region} team intends to review first-quarter baselines, summer demand and autumn range changes in separate account meetings. These are broad planning windows, not promotion dates. Product-specific offers are recorded separately in the structured promotions table. A generic annual plan cannot demonstrate that a discount, display or reset occurred in a particular store or week. Dates and execution status must be checked against the relevant brief before the agent describes an event as completed.",
                f"Category priorities. Discussion with {retailer} will cover plant-based drinks, granola, soups, snacks, yogurt and cooking sauces where the account has records. Ambient products and chilled products have different ordering and handling requirements. The commercial team proposes reviewing {focus['category'].lower()} first, but this does not rank its actual performance against other categories. Units, selling price, availability and shipment fill measure different aspects of trading. Combining them requires explicit aggregation conventions, and no single metric identifies the mechanism behind a sales change.",
                f"Operational review. The {region} team would ask {retailer} for receiving exceptions, backroom inventory checks and dated shelf observations if weekly availability weakened. The fictional shipment table is useful for practicing bounded queries, not confirming an unrecorded incident. Retailer comparisons should consider geography, product mix and reporting coverage. In particular, no Northeast OAT-1 rows are provided, and the controlled Midwest oat-drink scenario contains only NorthMart and FreshCo. The annual plan does not override those deliberate data boundaries.",
                f"Evidence and accountability. Account managers own the proposed {initiative}, while supply colleagues would review dispatch exceptions and analysts would prepare descriptive comparisons. This document does not contain an approval log, completed-store list or estimate of incremental sales. Any answer based on it should identify {retailer}, {region} and the annual planning scope. Claims about executed events or causal impact need more specific evidence. When retrieval returns this plan for a monthly product question, use only its relevant context and disclose the mismatch in scope.",
                f"Decision criteria. The account team will consider a recommendation only after reviewing comparable periods, recorded promotions, stock observations and the limitations of the available evidence. An agent should cite DOC-ACCOUNT-{region.upper()}-{retailer.upper()}-2025 for the proposed activity, not for an unsupported outcome. If a question is missing its product or dates, request clarification. If the filtered data is absent, report that absence without extrapolating from another region. The objective is a verifiable account summary that distinguishes observations, plans and unresolved questions.",
            ], region=region, retailer=retailer))
    return documents


def build_northstar_rows():
    """Return deterministic Python rows, also usable for fixture checks without Spark."""
    products = _products()
    weeks = [date(2025, 1, 5) + timedelta(weeks=number) for number in range(52)]
    sales, availability, promotions, shipments = [], [], [], []
    case_units = {"NorthMart": [150, 155, 145, 150, 95, 90, 85, 90],
                  "FreshCo": [100, 100, 105, 95, 105, 110, 115, 110]}
    case_rates = {"NorthMart": [0.98, 0.98, 0.97, 0.98, 0.82, 0.78, 0.74, 0.78],
                  "FreshCo": [0.97, 0.98, 0.97, 0.98, 0.98, 0.98, 0.99, 0.98]}
    case_weeks = [date(2025, 4, 6) + timedelta(weeks=number) for number in range(8)]
    for product_number, product in enumerate(products):
        product_id = product["product_id"]
        for region_number, region in enumerate(REGIONS):
            for retailer_number, retailer in enumerate(RETAILERS):
                if product_id == "OAT-1" and (region == "Northeast" or (region == "Midwest" and retailer not in case_units)):
                    continue
                for week_number, week in enumerate(weeks):
                    base = 85 + product_number * 11 + region_number * 17 + retailer_number * 23
                    seasonal = (week.month in (6, 7, 8)) * (35 if product_id.startswith("SNK") else -8)
                    seasonal += (week.month in (1, 2, 11, 12)) * (45 if product_id.startswith("SOUP") else 6)
                    variation = ((week_number * 13 + product_number * 7 + region_number * 5) % 31) - 15
                    units = max(0, base + seasonal + variation + week_number // 8)
                    rate = round(0.91 + ((week_number + product_number + retailer_number) % 8) * 0.01, 2)
                    if product_id == "OAT-1" and region == "Midwest" and week in case_weeks:
                        case_number = case_weeks.index(week)
                        units, rate = case_units[retailer][case_number], case_rates[retailer][case_number]
                    price = round(product["list_price"] * (1 + region_number * 0.01 - retailer_number * 0.02), 2)
                    sales.append((week, product_id, product["product_name"], region, retailer, units, price, round(units * price, 2)))
                    availability.append((week, product_id, region, retailer, rate))
                    ordered = units + 20 + (week_number % 4) * 5
                    shipped = ordered - ((week_number + product_number + region_number) % 7) * 3
                    shipments.append((week, product_id, region, retailer, ordered, shipped, round(shipped / ordered, 4)))
                if product_id == "OAT-1" and region == "Midwest":
                    if retailer == "NorthMart":
                        promotions.append((product_id, region, retailer, date(2025, 4, 1), date(2025, 4, 21), 10.0, "Spring oat-drink promotion."))
                    else:
                        promotions.append((product_id, region, retailer, date(2025, 4, 7), date(2025, 4, 13), 5.0, "Weekly featured-item promotion."))
                else:
                    for month in (2, 6, 9):
                        start = date(2025, month, 3 + (product_number + retailer_number) % 8)
                        promotions.append((product_id, region, retailer, start, start + timedelta(days=13),
                                           float(5 + ((product_number + region_number + retailer_number) % 4) * 5),
                                           f"{product['variant']} {product['category'].lower()} seasonal feature; planned offer, execution unverified."))
    return {
        "products": [tuple(product.values()) for product in products],
        "retailers": [(name, ("National grocery", "Fresh-focused grocery", "Value grocery", "Neighbourhood grocery")[number]) for number, name in enumerate(RETAILERS)],
        "sales_weekly": sales, "availability_weekly": availability,
        "promotions": promotions, "shipments_weekly": shipments,
        "documents": _documents(products),
    }


def build_northstar_dataframes(spark):
    """Create eight training DataFrames; split long documents into paragraph chunks with Spark."""
    from pyspark.sql import functions as functions

    schemas = {
        "products": "product_id string, product_name string, category string, variant string, pack_size string, list_price double, storage string, shelf_life_days int",
        "retailers": "retailer string, channel string",
        "sales_weekly": "week_start date, product_id string, product_name string, region string, retailer string, units_sold long, unit_price double, sales_value double",
        "availability_weekly": "week_start date, product_id string, region string, retailer string, in_stock_rate double",
        "promotions": "product_id string, region string, retailer string, start_date date, end_date date, discount_percent double, description string",
        "shipments_weekly": "week_start date, product_id string, region string, retailer string, units_ordered long, units_shipped long, fill_rate double",
        "documents": "document_id string, title string, document_text string, product_id string, region string, retailer string",
    }
    rows = build_northstar_rows()
    frames = {name: spark.createDataFrame(rows[name], schema) for name, schema in schemas.items()}
    frames["document_chunks"] = frames["documents"].select(
        "document_id", "title", "product_id", "region", "retailer",
        functions.posexplode(functions.split("document_text", r"\n\n+")).alias("chunk_index", "chunk_text"),
    ).withColumn("chunk_id", functions.concat("document_id", functions.lit("-"), functions.col("chunk_index"))).select(
        "chunk_id", "document_id", "title", "chunk_text", "chunk_index", "product_id", "region", "retailer"
    )
    return frames


def write_northstar_tables(spark, catalog: str, schema: str):
    """Overwrite all eight workshop Delta tables and return qualified names/counts.

    Use a dedicated schema: existing tables with these names are replaced. The
    catalog must exist. Change data feed supports a pre-created Delta Sync index.
    """
    for label, value in (("catalog", catalog), ("schema", schema)):
        if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", value):
            raise ValueError(f"{label} must be a simple Unity Catalog identifier")
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS `{catalog}`.`{schema}`")
    report = {}
    for name, dataframe in build_northstar_dataframes(spark).items():
        qualified_name = f"{catalog}.{schema}.{name}"
        dataframe.write.format("delta").mode("overwrite").option("overwriteSchema", "true").option(
            "delta.enableChangeDataFeed", "true"
        ).saveAsTable(qualified_name)
        report[name] = {"table": qualified_name, "rows": spark.table(qualified_name).count()}
    return report